"""Request and response schemas for assessments."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ScanType(StrEnum):
    SAST = "sast"
    DEPENDENCY = "dependency"
    SECRET = "secret"


class AssessmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    repository_url: HttpUrl
    scan_types: list[ScanType] = Field(
        default_factory=lambda: list(ScanType), min_length=1
    )


class AssessmentRead(BaseModel):
    id: str
    name: str
    repository_url: str
    status: str
    scan_types: list[ScanType]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
