from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Instrument
from api.schemas import InstrumentCreate, InstrumentUpdate, InstrumentResponse

router = APIRouter(prefix="/api/instruments", tags=["instruments"])

@router.get("", response_model=List[InstrumentResponse])
def list_instruments(db: Session = Depends(get_db)):
    return db.query(Instrument).all()

@router.post("", response_model=InstrumentResponse, status_code=201)
def create_instrument(data: InstrumentCreate, db: Session = Depends(get_db)):
    existing = db.query(Instrument).filter(Instrument.instrument_code == data.instrument_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Instrument code already exists")
    instrument = Instrument(**data.model_dump())
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument

@router.get("/{instrument_id}", response_model=InstrumentResponse)
def get_instrument(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument

@router.put("/{instrument_id}", response_model=InstrumentResponse)
def update_instrument(instrument_id: int, data: InstrumentUpdate, db: Session = Depends(get_db)):
    instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(instrument, key, value)
    db.commit()
    db.refresh(instrument)
    return instrument

@router.delete("/{instrument_id}")
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    db.delete(instrument)
    db.commit()
    return {"message": "Instrument deleted"}
