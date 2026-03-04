from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from database import get_db
from models import Sample, Result, Order

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/{sample_id}")
def generate_report(sample_id: int, db: Session = Depends(get_db)):
    """Generate a simple text-based report for a sample"""
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    results = db.query(Result).filter(Result.sample_id == sample_id).all()

    # Build report as JSON (PDF generation requires reportlab which may fail on deploy)
    report_data = {
        "report_type": "Lab Report",
        "lab_name": "Enigma LIMS",
        "sample": {
            "id": sample.sample_id,
            "type": sample.sample_type,
            "collection_date": sample.collection_date.isoformat(),
            "status": sample.status
        },
        "patient": {
            "name": sample.patient.name if sample.patient else "Unknown",
            "age": sample.patient.age if sample.patient else None,
            "gender": sample.patient.gender if sample.patient else None
        },
        "results": [
            {
                "test_name": r.test.test_name if r.test else "Unknown",
                "result_value": r.result_value,
                "unit": r.unit,
                "reference_range": f"{r.test.reference_min}-{r.test.reference_max}" if r.test and r.test.reference_min else "N/A",
                "status": r.status,
                "interpretation": r.interpretation
            }
            for r in results
        ],
        "generated_at": __import__("datetime").datetime.utcnow().isoformat()
    }
    return report_data

@router.get("")
def list_reports(db: Session = Depends(get_db)):
    """Get list of completed samples (available for report)"""
    samples = db.query(Sample).filter(
        Sample.status.in_(["completed", "approved"])
    ).order_by(Sample.created_at.desc()).limit(50).all()

    return [
        {
            "id": s.id,
            "sample_id": s.sample_id,
            "patient_name": s.patient.name if s.patient else "Unknown",
            "sample_type": s.sample_type,
            "status": s.status,
            "collection_date": s.collection_date.isoformat(),
            "result_count": len(s.results)
        }
        for s in samples
    ]
