from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Patient, Doctor, Sample, Order, Result
from api.schemas import PatientCreate, PatientUpdate, PatientResponse, PatientHistoryEntry

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.get("", response_model=List[PatientResponse])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    if search:
        query = query.filter(Patient.name.ilike(f"%{search}%"))
    patients = query.offset(skip).limit(limit).all()
    result = []
    for p in patients:
        data = PatientResponse.model_validate(p)
        if p.doctor:
            data.doctor_name = p.doctor.name
        result.append(data)
    return result

@router.post("", response_model=PatientResponse, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    resp = PatientResponse.model_validate(patient)
    if patient.doctor:
        resp.doctor_name = patient.doctor.name
    return resp

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    resp = PatientResponse.model_validate(patient)
    if patient.doctor:
        resp.doctor_name = patient.doctor.name
    return resp

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, data: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    resp = PatientResponse.model_validate(patient)
    if patient.doctor:
        resp.doctor_name = patient.doctor.name
    return resp

@router.get("/{patient_id}/history", response_model=List[PatientHistoryEntry])
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    samples = db.query(Sample).filter(Sample.patient_id == patient_id).order_by(Sample.created_at.desc()).all()
    result = []
    for s in samples:
        order_count = db.query(Order).filter(Order.sample_id == s.id).count()
        results = db.query(Result).filter(Result.sample_id == s.id).all()
        has_critical = any(r.status == "critical" for r in results)
        entry = PatientHistoryEntry(
            id=s.id,
            sample_id=s.sample_id,
            sample_type=s.sample_type,
            collection_date=s.collection_date,
            status=s.status,
            priority=getattr(s, 'priority', 'routine'),
            test_count=order_count,
            result_count=len(results),
            has_critical=has_critical
        )
        result.append(entry)
    return result


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}
