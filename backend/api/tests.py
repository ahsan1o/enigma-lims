from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Test, TestReferenceRange
from api.schemas import TestCreate, TestUpdate, TestResponse, ReferenceRangeCreate, ReferenceRangeResponse
from utils.auth import require_admin

router = APIRouter(prefix="/api/tests", tags=["tests"])

@router.get("", response_model=List[TestResponse])
def list_tests(
    skip: int = 0,
    limit: int = 200,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Test)
    if search:
        query = query.filter(Test.test_name.ilike(f"%{search}%") | Test.test_code.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.post("", response_model=TestResponse, status_code=201)
def create_test(data: TestCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    existing = db.query(Test).filter(Test.test_code == data.test_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Test code already exists")
    test = Test(**data.model_dump())
    db.add(test)
    db.commit()
    db.refresh(test)
    return test

@router.get("/{test_id}", response_model=TestResponse)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.put("/{test_id}", response_model=TestResponse)
def update_test(test_id: int, data: TestUpdate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(test, key, value)
    db.commit()
    db.refresh(test)
    return test

@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(test)
    db.commit()
    return {"message": "Test deleted"}


# ─── Reference Range CRUD ─────────────────────────────────────────────────────

@router.get("/{test_id}/ranges", response_model=List[ReferenceRangeResponse])
def list_ranges(test_id: int, db: Session = Depends(get_db)):
    return db.query(TestReferenceRange).filter(TestReferenceRange.test_id == test_id).all()

@router.post("/{test_id}/ranges", response_model=ReferenceRangeResponse, status_code=201)
def create_range(test_id: int, data: ReferenceRangeCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    r = TestReferenceRange(test_id=test_id, **data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.put("/{test_id}/ranges/{range_id}", response_model=ReferenceRangeResponse)
def update_range(test_id: int, range_id: int, data: ReferenceRangeCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    r = db.query(TestReferenceRange).filter(
        TestReferenceRange.id == range_id,
        TestReferenceRange.test_id == test_id
    ).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reference range not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r

@router.delete("/{test_id}/ranges/{range_id}")
def delete_range(test_id: int, range_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    r = db.query(TestReferenceRange).filter(
        TestReferenceRange.id == range_id,
        TestReferenceRange.test_id == test_id
    ).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reference range not found")
    db.delete(r)
    db.commit()
    return {"message": "Deleted"}
