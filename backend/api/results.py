from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Result, Order, Test, User
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

@router.get("", response_model=List[ResultResponse])
def list_results(
    sample_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Result)
    if sample_id:
        query = query.filter(Result.sample_id == sample_id)
    if status:
        query = query.filter(Result.status == status)
    results = query.order_by(Result.created_at.desc()).offset(skip).limit(limit).all()

    out = []
    for r in results:
        data = ResultResponse.model_validate(r)
        if r.test:
            data.test_name = r.test.test_name
        if r.entered_by_user:
            data.entered_by_name = r.entered_by_user.full_name
        if r.approved_by_user:
            data.approved_by_name = r.approved_by_user.full_name
        out.append(data)
    return out

@router.post("", response_model=ResultResponse, status_code=201)
def create_result(data: ResultCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    test = db.query(Test).filter(Test.id == data.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    status = _determine_status(data.result_value, test)
    unit = data.unit or test.unit

    result = Result(
        order_id=data.order_id,
        sample_id=data.sample_id,
        test_id=data.test_id,
        result_value=data.result_value,
        unit=unit,
        status=status,
        interpretation=data.interpretation,
        entered_date=datetime.utcnow(),
        machine_generated=False
    )
    db.add(result)

    # Update order status
    order.status = "completed"
    db.commit()
    db.refresh(result)

    resp = ResultResponse.model_validate(result)
    if test:
        resp.test_name = test.test_name
    return resp

@router.put("/{result_id}", response_model=ResultResponse)
def update_result(result_id: int, data: ResultCreate, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    test = db.query(Test).filter(Test.id == result.test_id).first()
    result.result_value = data.result_value
    result.unit = data.unit or (test.unit if test else result.unit)
    result.interpretation = data.interpretation
    if test:
        result.status = _determine_status(data.result_value, test)
    db.commit()
    db.refresh(result)
    resp = ResultResponse.model_validate(result)
    if test:
        resp.test_name = test.test_name
    return resp

@router.post("/{result_id}/approve", response_model=ResultResponse)
def approve_result(result_id: int, data: ResultApprove, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    result.approved_date = datetime.utcnow()
    result.qc_passed = True
    if data.comments:
        result.interpretation = (result.interpretation or "") + f"\nApproval note: {data.comments}"
    db.commit()
    db.refresh(result)
    resp = ResultResponse.model_validate(result)
    if result.test:
        resp.test_name = result.test.test_name
    return resp
