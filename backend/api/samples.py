from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Sample, Patient
from api.schemas import SampleCreate, SampleStatusUpdate, SampleReject, SampleResponse
from services.barcode_service import generate_sample_id

router = APIRouter(prefix="/api/samples", tags=["samples"])

@router.get("", response_model=List[SampleResponse])
def list_samples(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Sample).options(joinedload(Sample.patient))
    if status:
        query = query.filter(Sample.status == status)
    if search:
        query = query.join(Patient).filter(Patient.name.ilike(f"%{search}%"))
    samples = query.order_by(Sample.priority.desc(), Sample.created_at.desc()).offset(skip).limit(limit).all()
    result = []
    for s in samples:
        data = SampleResponse.model_validate(s)
        if s.patient:
            data.patient_name = s.patient.name
        result.append(data)
    return result

@router.post("", response_model=SampleResponse, status_code=201)
def create_sample(data: SampleCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    sample_data = data.model_dump()
    sample_data["sample_id"] = generate_sample_id()
    sample_data["received_date"] = datetime.utcnow()
    sample_data["status"] = "pending"

    sample = Sample(**sample_data)
    db.add(sample)
    db.commit()
    db.refresh(sample)

    resp = SampleResponse.model_validate(sample)
    resp.patient_name = patient.name
    return resp

@router.get("/{sample_id}", response_model=SampleResponse)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    resp = SampleResponse.model_validate(sample)
    if sample.patient:
        resp.patient_name = sample.patient.name
    return resp

@router.put("/{sample_id}/status", response_model=SampleResponse)
def update_sample_status(sample_id: int, data: SampleStatusUpdate, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.status = data.status
    db.commit()
    db.refresh(sample)
    resp = SampleResponse.model_validate(sample)
    if sample.patient:
        resp.patient_name = sample.patient.name
    return resp

@router.put("/{sample_id}/reject", response_model=SampleResponse)
def reject_sample(sample_id: int, data: SampleReject, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.status = "rejected"
    sample.rejection_reason = data.rejection_reason
    db.commit()
    db.refresh(sample)
    resp = SampleResponse.model_validate(sample)
    if sample.patient:
        resp.patient_name = sample.patient.name
    return resp


@router.delete("/{sample_id}")
def delete_sample(sample_id: int, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    db.delete(sample)
    db.commit()
    return {"message": "Sample deleted"}
