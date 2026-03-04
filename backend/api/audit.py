from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import AuditLog, User
from api.schemas import AuditLogResponse

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("", response_model=List[AuditLogResponse])
def list_audit_logs(
    skip: int = 0,
    limit: int = 200,
    table_name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if table_name:
        query = query.filter(AuditLog.table_name == table_name)
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    result = []
    for log in logs:
        resp = AuditLogResponse.model_validate(log)
        if log.user:
            resp.username = log.user.username
        result.append(resp)
    return result
