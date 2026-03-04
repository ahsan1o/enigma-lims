from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from models import Order, Sample, Test, Doctor, Patient
from api.schemas import OrderCreate, OrderResponse, BulkOrderCreate

router = APIRouter(prefix="/api/orders", tags=["orders"])


def _enrich_order(o: Order) -> OrderResponse:
    data = OrderResponse.model_validate(o)
    if o.sample:
        data.sample_barcode = o.sample.sample_id
        if o.sample.patient:
            data.patient_name = o.sample.patient.name
    if o.test:
        data.test_name = o.test.test_name
        data.test_code = o.test.test_code
        data.test_price = o.test.price
    if o.doctor:
        data.doctor_name = o.doctor.name
    return data


@router.get("", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 200,
    status: Optional[str] = Query(None),
    sample_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Order).options(
        joinedload(Order.sample).joinedload(Sample.patient),
        joinedload(Order.test),
        joinedload(Order.doctor)
    )
    if status:
        query = query.filter(Order.status == status)
    if sample_id:
        query = query.filter(Order.sample_id == sample_id)
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return [_enrich_order(o) for o in orders]


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    sample = db.query(Sample).options(joinedload(Sample.patient)).filter(Sample.id == data.sample_id).first()
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

    order = db.query(Order).options(
        joinedload(Order.sample).joinedload(Sample.patient),
        joinedload(Order.test),
        joinedload(Order.doctor)
    ).filter(Order.id == order.id).first()
    return _enrich_order(order)


@router.post("/bulk", response_model=List[OrderResponse], status_code=201)
def create_bulk_orders(data: BulkOrderCreate, db: Session = Depends(get_db)):
    """Create multiple test orders for a sample in one request."""
    sample = db.query(Sample).options(joinedload(Sample.patient)).filter(Sample.id == data.sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    created_ids = []
    for test_id in data.test_ids:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            continue
        existing = db.query(Order).filter(
            Order.sample_id == data.sample_id,
            Order.test_id == test_id
        ).first()
        if existing:
            created_ids.append(existing.id)
            continue
        order = Order(
            sample_id=data.sample_id,
            test_id=test_id,
            doctor_id=data.doctor_id,
            priority=data.priority,
            status="pending"
        )
        db.add(order)
        db.flush()
        created_ids.append(order.id)

    db.commit()

    orders = db.query(Order).options(
        joinedload(Order.sample).joinedload(Sample.patient),
        joinedload(Order.test),
        joinedload(Order.doctor)
    ).filter(Order.id.in_(created_ids)).all()
    return [_enrich_order(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).options(
        joinedload(Order.sample).joinedload(Sample.patient),
        joinedload(Order.test),
        joinedload(Order.doctor)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _enrich_order(order)


@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    return {"message": "Order status updated"}
