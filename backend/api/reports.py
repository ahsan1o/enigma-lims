from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exists
from datetime import datetime
from database import get_db
from models import Sample, Result, Order

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/{sample_id}")
def generate_report(sample_id: int, db: Session = Depends(get_db)):
    """Generate a full report for a sample including test prices and reference ranges."""
    sample = db.query(Sample).options(
        joinedload(Sample.patient)
    ).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    results = db.query(Result).options(
        joinedload(Result.test)
    ).filter(Result.sample_id == sample_id).all()

    result_items = []
    total_amount = 0.0
    for r in results:
        test = r.test
        price = (test.price or 0.0) if test else 0.0
        total_amount += price

        # Build reference range string
        ref_range = "N/A"
        if test and test.reference_min is not None and test.reference_max is not None:
            ref_range = f"{test.reference_min} – {test.reference_max}"
        elif test and test.reference_min is not None:
            ref_range = f"≥ {test.reference_min}"
        elif test and test.reference_max is not None:
            ref_range = f"≤ {test.reference_max}"

        result_items.append({
            "test_name": test.test_name if test else "Unknown",
            "test_code": test.test_code if test else "",
            "result_value": r.result_value,
            "unit": r.unit or (test.unit if test else ""),
            "reference_range": ref_range,
            "reference_min": test.reference_min if test else None,
            "reference_max": test.reference_max if test else None,
            "critical_min": test.critical_min if test else None,
            "critical_max": test.critical_max if test else None,
            "status": r.status,
            "interpretation": r.interpretation,
            "price": price,
            "approved_date": r.approved_date.isoformat() if r.approved_date else None,
        })

    return {
        "report_type": "Lab Report",
        "lab_name": "Enigma LIMS",
        "sample": {
            "id": sample.sample_id,
            "type": sample.sample_type,
            "collection_date": sample.collection_date.isoformat(),
            "status": sample.status,
            "priority": sample.priority or "routine"
        },
        "patient": {
            "name": sample.patient.name if sample.patient else "Unknown",
            "age": sample.patient.age if sample.patient else None,
            "gender": sample.patient.gender if sample.patient else None,
            "phone": sample.patient.phone if sample.patient else None
        },
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
        joinedload(Sample.patient)
    ).filter(
        exists().where(Result.sample_id == Sample.id)
    ).order_by(Sample.created_at.desc()).limit(200).all()

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
            "referring_doctor": None
        }
        for s in samples
    ]
