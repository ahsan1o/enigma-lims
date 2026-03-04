from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Result, Order, Test, User, Sample, TestReferenceRange
from api.schemas import (
    ResultCreate, ResultApprove, ResultResponse,
    BulkResultItem, MachineResultsInput
)
from utils.auth import get_current_user

router = APIRouter(prefix="/api/results", tags=["results"])


def _get_reference_range(test_id: int, age: Optional[int], gender: Optional[str], db: Session):
    """Return the best-matching TestReferenceRange for a patient's demographics."""
    ranges = db.query(TestReferenceRange).filter(TestReferenceRange.test_id == test_id).all()
    if not ranges:
        return None
    g = None
    if gender:
        g = gender.strip().upper()[0] if gender.strip() else None  # "M" or "F"
    best = None
    for r in ranges:
        gender_match = (r.gender == "Any") or (g and r.gender.upper()[0] == g)
        age_match = (age is None) or (r.min_age <= age <= r.max_age)
        if gender_match and age_match:
            if best is None:
                best = r
            elif r.gender != "Any" and best.gender == "Any":
                best = r  # prefer gender-specific
    return best


def _determine_status(result_value: str, ref_range) -> str:
    """Determine normal/abnormal/critical status from a reference range object."""
    try:
        val = float(result_value)
        if ref_range:
            if ref_range.critical_min is not None and val < ref_range.critical_min:
                return "critical"
            if ref_range.critical_max is not None and val > ref_range.critical_max:
                return "critical"
            if ref_range.ref_min is not None and val < ref_range.ref_min:
                return "abnormal"
            if ref_range.ref_max is not None and val > ref_range.ref_max:
                return "abnormal"
            return "normal"
        return "normal"
    except (ValueError, TypeError):
        return "normal"


def _enrich(data: ResultResponse, r: Result) -> ResultResponse:
    """Attach test reference ranges, price, and patient name to a ResultResponse."""
    if r.test:
        data.test_name = r.test.test_name
        data.test_code = r.test.test_code
        data.price = r.test.price
        # Fallback: use flat test values if no patient-specific range was used
        data.reference_min = r.test.reference_min
        data.reference_max = r.test.reference_max
        data.critical_min = r.test.critical_min
        data.critical_max = r.test.critical_max
    if r.entered_by_user:
        data.entered_by_name = r.entered_by_user.full_name
    if r.approved_by_user:
        data.approved_by_name = r.approved_by_user.full_name
    if r.sample and r.sample.patient:
        data.patient_name = r.sample.patient.name
    return data


def _maybe_complete_sample(sample_id: int, db: Session):
    """Mark sample completed once all its orders are done."""
    pending = db.query(Order).filter(
        Order.sample_id == sample_id,
        Order.status != "completed"
    ).count()
    if pending == 0:
        sample = db.query(Sample).filter(Sample.id == sample_id).first()
        if sample and sample.status not in ("completed", "approved"):
            sample.status = "completed"


@router.get("", response_model=List[ResultResponse])
def list_results(
    sample_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    query = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.entered_by_user),
        joinedload(Result.approved_by_user),
        joinedload(Result.sample).joinedload(Sample.patient)
    )
    if sample_id:
        query = query.filter(Result.sample_id == sample_id)
    if status:
        query = query.filter(Result.status == status)
    results = query.order_by(Result.created_at.desc()).offset(skip).limit(limit).all()
    return [_enrich(ResultResponse.model_validate(r), r) for r in results]


@router.post("", response_model=ResultResponse, status_code=201)
def create_result(data: ResultCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    test = db.query(Test).filter(Test.id == data.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # Look up patient demographics for age/gender-specific reference range
    sample = db.query(Sample).options(joinedload(Sample.patient)).filter(Sample.id == data.sample_id).first()
    patient = sample.patient if sample else None
    ref_range = _get_reference_range(test.id, patient.age if patient else None, patient.gender if patient else None, db)

    result_status = _determine_status(data.result_value, ref_range)
    unit = data.unit or test.unit

    result = Result(
        order_id=data.order_id,
        sample_id=data.sample_id,
        test_id=data.test_id,
        result_value=data.result_value,
        unit=unit,
        status=result_status,
        interpretation=data.interpretation,
        entered_date=datetime.utcnow(),
        machine_generated=False
    )
    db.add(result)
    order.status = "completed"
    db.flush()
    _maybe_complete_sample(data.sample_id, db)
    db.commit()
    db.refresh(result)

    resp = ResultResponse.model_validate(result)
    return _enrich(resp, result)


@router.post("/bulk", response_model=List[ResultResponse], status_code=201)
def create_bulk_results(items: List[BulkResultItem], db: Session = Depends(get_db)):
    """Submit results for multiple tests on a sample at once (machine-like entry)."""
    created = []
    sample_ids = set()

    for item in items:
        order = db.query(Order).filter(Order.id == item.order_id).first()
        if not order:
            continue
        test = db.query(Test).filter(Test.id == item.test_id).first()
        if not test:
            continue

        sample = db.query(Sample).options(joinedload(Sample.patient)).filter(Sample.id == item.sample_id).first()
        patient = sample.patient if sample else None
        ref_range = _get_reference_range(test.id, patient.age if patient else None, patient.gender if patient else None, db)
        result_status = _determine_status(item.result_value, ref_range)

        result = Result(
            order_id=item.order_id,
            sample_id=item.sample_id,
            test_id=item.test_id,
            result_value=item.result_value,
            unit=item.unit or test.unit,
            status=result_status,
            interpretation=item.interpretation,
            entered_date=datetime.utcnow(),
            machine_generated=False
        )
        db.add(result)
        order.status = "completed"
        sample_ids.add(item.sample_id)
        created.append(result)
        db.flush()

    for sid in sample_ids:
        _maybe_complete_sample(sid, db)

    db.commit()

    final = []
    for r in created:
        db.refresh(r)
        # Re-load relationships
        r = db.query(Result).options(
            joinedload(Result.test),
            joinedload(Result.entered_by_user),
            joinedload(Result.approved_by_user),
            joinedload(Result.sample).joinedload(Sample.patient)
        ).filter(Result.id == r.id).first()
        final.append(_enrich(ResultResponse.model_validate(r), r))
    return final


@router.post("/machine-input")
def receive_machine_results(data: MachineResultsInput, db: Session = Depends(get_db)):
    """
    Receive results from an analyzer (HL7/ASTM adapter or CSV import).
    Matches sample by barcode string, tests by test_code, fills pending orders.
    """
    sample = db.query(Sample).options(joinedload(Sample.patient)).filter(
        Sample.sample_id == data.sample_barcode
    ).first()
    if not sample:
        raise HTTPException(status_code=404, detail=f"Sample '{data.sample_barcode}' not found")

    patient = sample.patient
    inserted = []
    not_found = []
    already_done = []

    for item in data.results:
        test = db.query(Test).filter(Test.test_code == item.test_code).first()
        if not test:
            not_found.append(item.test_code)
            continue

        order = db.query(Order).filter(
            Order.sample_id == sample.id,
            Order.test_id == test.id,
            Order.status == "pending"
        ).first()
        if not order:
            already_done.append(item.test_code)
            continue

        ref_range = _get_reference_range(test.id, patient.age if patient else None, patient.gender if patient else None, db)
        status = _determine_status(item.result_value, ref_range)

        result = Result(
            order_id=order.id,
            sample_id=sample.id,
            test_id=test.id,
            result_value=item.result_value,
            unit=item.unit or test.unit,
            status=status,
            entered_date=datetime.utcnow(),
            machine_generated=True
        )
        db.add(result)
        order.status = "completed"
        inserted.append(item.test_code)
        db.flush()

    _maybe_complete_sample(sample.id, db)
    db.commit()

    return {
        "sample": data.sample_barcode,
        "inserted": inserted,
        "not_found": not_found,
        "already_completed": already_done,
        "total_inserted": len(inserted)
    }


@router.put("/{result_id}", response_model=ResultResponse)
def update_result(result_id: int, data: ResultCreate, db: Session = Depends(get_db)):
    result = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.sample).joinedload(Sample.patient)
    ).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    test = result.test
    patient = result.sample.patient if result.sample else None
    ref_range = _get_reference_range(test.id if test else 0, patient.age if patient else None, patient.gender if patient else None, db)
    result.result_value = data.result_value
    result.unit = data.unit or (test.unit if test else result.unit)
    result.interpretation = data.interpretation
    result.status = _determine_status(data.result_value, ref_range) if test else result.status
    db.commit()
    db.refresh(result)
    return _enrich(ResultResponse.model_validate(result), result)


@router.post("/{result_id}/approve", response_model=ResultResponse)
def approve_result(
    result_id: int,
    data: ResultApprove,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.sample).joinedload(Sample.patient)
    ).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    result.approved_date = datetime.utcnow()
    result.approved_by = current_user.get("user_id")
    result.qc_passed = True
    if data.comments:
        result.interpretation = (result.interpretation or "") + f"\nApproval note: {data.comments}"
    db.commit()
    db.refresh(result)
    return _enrich(ResultResponse.model_validate(result), result)
