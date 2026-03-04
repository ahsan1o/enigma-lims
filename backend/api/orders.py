from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from models import Order, Sample, Test, Doctor, Patient
from api.schemas import OrderCreate, OrderResponse

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Order).options(
        joinedload(Order.sample).joinedload(Sample.patient),
        joinedload(Order.test),
        joinedload(Order.doctor)
    )
    if status:
        query = query.filter(Order.status == status)
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    result = []
    for o in orders:
        data = OrderResponse.model_validate(o)
        if o.sample and o.sample.patient:
            data.patient_name = o.sample.patient.name
        if o.test:
            data.test_name = o.test.test_name
        if o.doctor:
            data.doctor_name = o.doctor.name
        result.append(data)
    return result

@router.post("", response_model=OrderResponse, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == data.sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    test = db.query(Test).filter(Test.id == data.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first() if data.doctor_id else None
    if data.doctor_id and not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    order = Order(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)

    resp = OrderResponse.model_validate(order)
    if sample.patient:
        resp.patient_name = sample.patient.name
    resp.test_name = test.test_name
    resp.doctor_name = doctor.name if doctor else None
    return resp

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    resp = OrderResponse.model_validate(order)
    if order.sample and order.sample.patient:
        resp.patient_name = order.sample.patient.name
    if order.test:
        resp.test_name = order.test.test_name
    if order.doctor:
        resp.doctor_name = order.doctor.name
    return resp

@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return {"message": "Order status updated"}
