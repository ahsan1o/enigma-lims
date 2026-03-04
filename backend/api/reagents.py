from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Reagent, Instrument
from api.schemas import ReagentCreate, ReagentUpdate, ReagentResponse

router = APIRouter(prefix="/api/reagents", tags=["reagents"])


def _build_reagent_response(r: Reagent) -> ReagentResponse:
    resp = ReagentResponse.model_validate(r)
    resp.low_stock = r.current_stock <= r.min_stock_level
    if r.instrument:
        resp.instrument_name = r.instrument.instrument_name
    return resp


@router.get("", response_model=List[ReagentResponse])
def list_reagents(
    low_stock_only: bool = Query(False),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(Reagent)
    if active_only:
        query = query.filter(Reagent.is_active == True)
    reagents = query.order_by(Reagent.name).all()
    result = [_build_reagent_response(r) for r in reagents]
    if low_stock_only:
        result = [r for r in result if r.low_stock]
    return result


@router.post("", response_model=ReagentResponse, status_code=201)
def create_reagent(data: ReagentCreate, db: Session = Depends(get_db)):
    reagent = Reagent(**data.model_dump())
    db.add(reagent)
    db.commit()
    db.refresh(reagent)
    return _build_reagent_response(reagent)


@router.get("/{reagent_id}", response_model=ReagentResponse)
def get_reagent(reagent_id: int, db: Session = Depends(get_db)):
    r = db.query(Reagent).filter(Reagent.id == reagent_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reagent not found")
    return _build_reagent_response(r)


@router.put("/{reagent_id}", response_model=ReagentResponse)
def update_reagent(reagent_id: int, data: ReagentUpdate, db: Session = Depends(get_db)):
    r = db.query(Reagent).filter(Reagent.id == reagent_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reagent not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(r, key, value)
    db.commit()
    db.refresh(r)
    return _build_reagent_response(r)


@router.delete("/{reagent_id}")
def delete_reagent(reagent_id: int, db: Session = Depends(get_db)):
    r = db.query(Reagent).filter(Reagent.id == reagent_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reagent not found")
    db.delete(r)
    db.commit()
    return {"message": "Reagent deleted"}
