from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Doctor
from api.schemas import DoctorCreate, DoctorUpdate, DoctorResponse

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

@router.get("", response_model=List[DoctorResponse])
def list_doctors(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Doctor)
    if search:
        query = query.filter(Doctor.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.post("", response_model=DoctorResponse, status_code=201)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    existing = db.query(Doctor).filter(Doctor.registration_number == data.registration_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Registration number already exists")
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, data: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted"}
