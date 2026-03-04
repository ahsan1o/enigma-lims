from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from database import get_db
from models import Patient, Sample, Result, Order, Test, Instrument, User
from api.schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    today = date.today()

    total_patients = db.query(func.count(Patient.id)).scalar()

    samples_today = db.query(func.count(Sample.id)).filter(
        func.date(Sample.created_at) == today
    ).scalar()

    pending_results = db.query(func.count(Order.id)).filter(
        Order.status == "pending"
    ).scalar()

    completed_today = db.query(func.count(Sample.id)).filter(
        Sample.status == "completed",
        func.date(Sample.updated_at) == today
    ).scalar()

    total_tests = db.query(func.count(Test.id)).scalar()
    total_instruments = db.query(func.count(Instrument.id)).scalar()

    return DashboardStats(
        total_patients=total_patients or 0,
        total_samples_today=samples_today or 0,
        pending_results=pending_results or 0,
        completed_today=completed_today or 0,
        total_tests=total_tests or 0,
        total_instruments=total_instruments or 0
    )

@router.get("/recent-samples")
def get_recent_samples(db: Session = Depends(get_db)):
    samples = db.query(Sample).order_by(Sample.created_at.desc()).limit(10).all()
    result = []
    for s in samples:
        result.append({
            "id": s.id,
            "sample_id": s.sample_id,
            "patient_name": s.patient.name if s.patient else "Unknown",
            "sample_type": s.sample_type,
            "status": s.status,
            "created_at": s.created_at.isoformat()
        })
    return result

@router.get("/recent-results")
def get_recent_results(db: Session = Depends(get_db)):
    results = db.query(Result).order_by(Result.created_at.desc()).limit(10).all()
    out = []
    for r in results:
        out.append({
            "id": r.id,
            "test_name": r.test.test_name if r.test else "Unknown",
            "result_value": r.result_value,
            "unit": r.unit,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        })
    return out
