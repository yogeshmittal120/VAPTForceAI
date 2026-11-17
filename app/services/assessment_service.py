"""Business operations for assessment records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate


def create_assessment(db: Session, payload: AssessmentCreate) -> Assessment:
    assessment = Assessment(
        name=payload.name,
        repository_url=str(payload.repository_url),
        scan_types=[scan_type.value for scan_type in payload.scan_types],
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


def list_assessments(db: Session, *, offset: int = 0, limit: int = 20) -> list[Assessment]:
    statement = (
        select(Assessment)
        .order_by(Assessment.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_assessment(db: Session, assessment_id: str) -> Assessment | None:
    return db.get(Assessment, assessment_id)
