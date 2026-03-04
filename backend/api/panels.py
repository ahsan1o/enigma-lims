from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import TestPanel, TestPanelItem, Test
from api.schemas import TestPanelCreate, TestPanelUpdate, TestPanelResponse, TestPanelItemResponse

router = APIRouter(prefix="/api/panels", tags=["panels"])


def _build_panel_response(panel: TestPanel) -> TestPanelResponse:
    resp = TestPanelResponse.model_validate(panel)
    resp.test_count = len(panel.panel_items)
    resp.items = []
    for item in panel.panel_items:
        item_resp = TestPanelItemResponse.model_validate(item)
        if item.test:
            item_resp.test_name = item.test.test_name
            item_resp.test_code = item.test.test_code
            item_resp.unit = item.test.unit
        resp.items.append(item_resp)
    return resp


@router.get("", response_model=List[TestPanelResponse])
def list_panels(
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(TestPanel)
    if active_only:
        query = query.filter(TestPanel.is_active == True)
    panels = query.order_by(TestPanel.name).all()
    return [_build_panel_response(p) for p in panels]


@router.post("", response_model=TestPanelResponse, status_code=201)
def create_panel(data: TestPanelCreate, db: Session = Depends(get_db)):
    panel = TestPanel(name=data.name, description=data.description)
    db.add(panel)
    db.flush()

    for test_id in data.test_ids:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail=f"Test {test_id} not found")
        db.add(TestPanelItem(panel_id=panel.id, test_id=test_id))

    db.commit()
    db.refresh(panel)
    return _build_panel_response(panel)


@router.get("/{panel_id}", response_model=TestPanelResponse)
def get_panel(panel_id: int, db: Session = Depends(get_db)):
    panel = db.query(TestPanel).filter(TestPanel.id == panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return _build_panel_response(panel)


@router.put("/{panel_id}", response_model=TestPanelResponse)
def update_panel(panel_id: int, data: TestPanelUpdate, db: Session = Depends(get_db)):
    panel = db.query(TestPanel).filter(TestPanel.id == panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    if data.name is not None:
        panel.name = data.name
    if data.description is not None:
        panel.description = data.description
    if data.is_active is not None:
        panel.is_active = data.is_active

    if data.test_ids is not None:
        # Replace all panel items
        db.query(TestPanelItem).filter(TestPanelItem.panel_id == panel_id).delete()
        for test_id in data.test_ids:
            db.add(TestPanelItem(panel_id=panel_id, test_id=test_id))

    db.commit()
    db.refresh(panel)
    return _build_panel_response(panel)


@router.delete("/{panel_id}")
def delete_panel(panel_id: int, db: Session = Depends(get_db)):
    panel = db.query(TestPanel).filter(TestPanel.id == panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    db.delete(panel)
    db.commit()
    return {"message": "Panel deleted"}
