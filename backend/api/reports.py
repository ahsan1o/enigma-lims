from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exists, or_
from datetime import datetime
from database import get_db
from models import Sample, Result, Order, TestReferenceRange

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _get_ref_range(test_id, age, gender, db):
    """Look up age/gender-specific reference range, fall back to Any if needed."""
    ranges = db.query(TestReferenceRange).filter(TestReferenceRange.test_id == test_id).all()
    if not ranges:
        return None
    g = gender.strip().upper()[0] if gender and gender.strip() else None
    best = None
    for r in ranges:
        gender_match = (r.gender == "Any") or (g and r.gender.upper()[0] == g)
        age_match = (age is None) or (r.min_age <= age <= r.max_age)
        if gender_match and age_match:
            if best is None:
                best = r
            elif r.gender != "Any" and best.gender == "Any":
                best = r
    return best


def _flag(value_str, ref_range, test):
    """Return H, L, C, or '' for a result value."""
    try:
        val = float(value_str)
    except (ValueError, TypeError):
        return ""
    rmin = ref_range.ref_min if ref_range else test.reference_min
    rmax = ref_range.ref_max if ref_range else test.reference_max
    cmin = ref_range.critical_min if ref_range else test.critical_min
    cmax = ref_range.critical_max if ref_range else test.critical_max
    if cmin is not None and val < cmin:
        return "C"
    if cmax is not None and val > cmax:
        return "C"
    if rmin is not None and val < rmin:
        return "L"
    if rmax is not None and val > rmax:
        return "H"
    return ""


@router.get("/{sample_id}")
def generate_report(sample_id: int, db: Session = Depends(get_db)):
    """Generate a full report for a sample including age/gender-adjusted reference ranges."""
    sample = db.query(Sample).options(
        joinedload(Sample.patient)
    ).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    results = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.entered_by_user),
        joinedload(Result.approved_by_user)
    ).filter(Result.sample_id == sample_id).all()

    # Get doctor name from a completed order for this sample (free-text doctor_name first, then FK)
    order_with_doctor = db.query(Order).filter(
        Order.sample_id == sample_id,
        or_(Order.doctor_id.isnot(None), Order.doctor_name.isnot(None))
    ).options(joinedload(Order.doctor)).first()
    referring_doctor = None
    if order_with_doctor:
        referring_doctor = order_with_doctor.doctor_name or (
            order_with_doctor.doctor.name if order_with_doctor.doctor else None
        )

    patient = sample.patient
    patient_age = patient.age if patient else None
    patient_gender = patient.gender if patient else None

    result_items = []
    total_amount = 0.0

    for r in results:
        test = r.test
        price = (test.price or 0.0) if test else 0.0
        total_amount += price

        # Age/gender-specific reference range
        ref_range = _get_ref_range(test.id, patient_age, patient_gender, db) if test else None

        # Fallback to flat test values if no specific range
        rmin = ref_range.ref_min if ref_range else (test.reference_min if test else None)
        rmax = ref_range.ref_max if ref_range else (test.reference_max if test else None)
        cmin = ref_range.critical_min if ref_range else (test.critical_min if test else None)
        cmax = ref_range.critical_max if ref_range else (test.critical_max if test else None)

        # Build reference range display string
        if rmin is not None and rmax is not None:
            ref_range_str = f"{rmin} – {rmax}"
        elif rmin is not None:
            ref_range_str = f"≥ {rmin}"
        elif rmax is not None:
            ref_range_str = f"≤ {rmax}"
        else:
            ref_range_str = "N/A"

        flag = _flag(r.result_value, ref_range, test) if test else ""

        result_items.append({
            "test_name": test.test_name if test else "Unknown",
            "test_code": test.test_code if test else "",
            "result_value": r.result_value,
            "unit": r.unit or (test.unit if test else ""),
            "reference_range": ref_range_str,
            "reference_min": rmin,
            "reference_max": rmax,
            "critical_min": cmin,
            "critical_max": cmax,
            "flag": flag,                         # "H", "L", "C", or ""
            "status": r.status,
            "interpretation": r.interpretation,
            "price": price,
            "entered_by": r.entered_by_user.full_name if r.entered_by_user else None,
            "approved_by": r.approved_by_user.full_name if r.approved_by_user else None,
            "approved_date": r.approved_date.isoformat() if r.approved_date else None,
        })

    return {
        "report_type": "Lab Report",
        "lab_name": "Enigma LIMS",
        "sample": {
            "id": sample.sample_id,
            "type": sample.sample_type,
            "collection_date": sample.collection_date.isoformat(),
            "received_date": sample.received_date.isoformat() if sample.received_date else None,
            "status": sample.status,
            "priority": sample.priority or "routine"
        },
        "patient": {
            "name": patient.name if patient else "Unknown",
            "age": patient.age if patient else None,
            "gender": patient.gender if patient else None,
            "phone": patient.phone if patient else None
        },
        "referring_doctor": referring_doctor,
        "results": result_items,
        "billing": {
            "total_amount": round(total_amount, 2),
            "currency": "PKR"
        },
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("")
def list_reports(db: Session = Depends(get_db)):
    """List all samples that have at least one result entered."""
    samples = db.query(Sample).options(
        joinedload(Sample.patient),
        joinedload(Sample.results)
    ).filter(
        exists().where(Result.sample_id == Sample.id)
    ).order_by(Sample.created_at.desc()).limit(200).all()

    # Batch-load referring doctors to avoid N+1
    sample_ids = [s.id for s in samples]
    orders_with_docs = db.query(Order).filter(
        Order.sample_id.in_(sample_ids),
        or_(Order.doctor_id.isnot(None), Order.doctor_name.isnot(None))
    ).options(joinedload(Order.doctor)).all()
    doctor_map = {}
    for o in orders_with_docs:
        if o.sample_id not in doctor_map:
            doc = o.doctor_name or (o.doctor.name if o.doctor else None)
            if doc:
                doctor_map[o.sample_id] = doc

    return [
        {
            "id": s.id,
            "sample_id": s.sample_id,
            "patient_name": s.patient.name if s.patient else "Unknown",
            "patient_phone": s.patient.phone if s.patient else None,
            "sample_type": s.sample_type,
            "status": s.status,
            "collection_date": s.collection_date.isoformat(),
            "result_count": len(s.results),
            "referring_doctor": doctor_map.get(s.id)
        }
        for s in samples
    ]
