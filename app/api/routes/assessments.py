"""Assessment management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assessment import AssessmentCreate, AssessmentRead
from app.services import assessment_service

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post(
    "", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED,
    summary="Create a security assessment",
)
def create_assessment(
    payload: AssessmentCreate, db: Session = Depends(get_db)
) -> AssessmentRead:
    return assessment_service.create_assessment(db, payload)


@router.get("", response_model=list[AssessmentRead], summary="List assessments")
def list_assessments(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[AssessmentRead]:
    return assessment_service.list_assessments(db, offset=offset, limit=limit)


@router.get(
    "/{assessment_id}", response_model=AssessmentRead,
    summary="Get an assessment by ID",
)
def get_assessment(
    assessment_id: str, db: Session = Depends(get_db)
) -> AssessmentRead:
    assessment = assessment_service.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment
