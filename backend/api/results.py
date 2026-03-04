from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Result, Order, Test, User, Sample
from api.schemas import ResultCreate, ResultApprove, ResultResponse

router = APIRouter(prefix="/api/results", tags=["results"])


def _determine_status(result_value: str, test: Test) -> str:
    """Determine normal/abnormal/critical status"""
    try:
        val = float(result_value)
        if test.critical_min and val < test.critical_min:
            return "critical"
        if test.critical_max and val > test.critical_max:
            return "critical"
        if test.reference_min and val < test.reference_min:
            return "abnormal"
        if test.reference_max and val > test.reference_max:
            return "abnormal"
        return "normal"
    except (ValueError, TypeError):
        return "normal"


def _enrich(data: ResultResponse, r: Result) -> ResultResponse:
    """Attach test reference ranges, price, and patient name to a ResultResponse."""
    if r.test:
        data.test_name = r.test.test_name
        data.test_code = r.test.test_code
        data.price = r.test.price
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

    result_status = _determine_status(data.result_value, test)
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


@router.put("/{result_id}", response_model=ResultResponse)
def update_result(result_id: int, data: ResultCreate, db: Session = Depends(get_db)):
    result = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.sample).joinedload(Sample.patient)
    ).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    test = result.test
    result.result_value = data.result_value
    result.unit = data.unit or (test.unit if test else result.unit)
    result.interpretation = data.interpretation
    if test:
        result.status = _determine_status(data.result_value, test)
    db.commit()
    db.refresh(result)
    return _enrich(ResultResponse.model_validate(result), result)


@router.post("/{result_id}/approve", response_model=ResultResponse)
def approve_result(result_id: int, data: ResultApprove, db: Session = Depends(get_db)):
    result = db.query(Result).options(
        joinedload(Result.test),
        joinedload(Result.sample).joinedload(Sample.patient)
    ).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    result.approved_date = datetime.utcnow()
    result.qc_passed = True
    if data.comments:
        result.interpretation = (result.interpretation or "") + f"\nApproval note: {data.comments}"
    db.commit()
    db.refresh(result)
    return _enrich(ResultResponse.model_validate(result), result)
