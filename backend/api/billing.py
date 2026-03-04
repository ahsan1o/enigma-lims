from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Invoice, InvoiceItem, Patient, Sample
from api.schemas import InvoiceCreate, InvoicePayment, InvoiceResponse, InvoiceItemResponse

router = APIRouter(prefix="/api/billing", tags=["billing"])


def _invoice_number() -> str:
    from datetime import datetime
    import random
    return f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000,9999)}"


def _build_invoice_response(inv: Invoice) -> InvoiceResponse:
    resp = InvoiceResponse.model_validate(inv)
    resp.balance = round(inv.total_amount - inv.paid_amount, 2)
    if inv.patient:
        resp.patient_name = inv.patient.name
    resp.items = [InvoiceItemResponse.model_validate(item) for item in inv.items]
    return resp


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Invoice)
    if status:
        query = query.filter(Invoice.status == status)
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    return [_build_invoice_response(inv) for inv in invoices]


@router.post("", response_model=InvoiceResponse, status_code=201)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    total = sum(item.amount for item in data.items)
    inv = Invoice(
        invoice_number=_invoice_number(),
        patient_id=data.patient_id,
        sample_id=data.sample_id,
        total_amount=total,
        paid_amount=0.0,
        status="unpaid",
        notes=data.notes
    )
    db.add(inv)
    db.flush()

    for item in data.items:
        db.add(InvoiceItem(
            invoice_id=inv.id,
            description=item.description,
            test_id=item.test_id,
            amount=item.amount
        ))

    db.commit()
    db.refresh(inv)
    return _build_invoice_response(inv)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return _build_invoice_response(inv)


@router.post("/{invoice_id}/pay", response_model=InvoiceResponse)
def record_payment(invoice_id: int, data: InvoicePayment, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    inv.paid_amount = min(inv.paid_amount + data.amount, inv.total_amount)
    if inv.paid_amount >= inv.total_amount:
        inv.status = "paid"
    elif inv.paid_amount > 0:
        inv.status = "partial"

    if data.notes:
        inv.notes = (inv.notes or "") + f"\nPayment: {data.notes}"

    db.commit()
    db.refresh(inv)
    return _build_invoice_response(inv)


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(inv)
    db.commit()
    return {"message": "Invoice deleted"}
