"""Deletion request context from dataset/deletion_requests.csv."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["DeletionReq", "ReportedStatus"]


ReportedStatus = Literal["COMPLETE", "PARTIALLY_COMPLETE", "NOT_STARTED"]


class DeletionReq(BaseModel):
    """Subset of deletion_requests.csv needed for audit routing.

    requested_at is intentionally omitted; audit_at is the cutoff.
    requestText is required for NOT_APPLICABLE detection.
    """

    model_config = ConfigDict(populate_by_name=True)

    caseId: str = Field(alias="case_id")
    email: str
    auditAt: str = Field(alias="audit_at")
    reportedStatus: ReportedStatus = Field(alias="reported_status")
    reportedAt: str = Field(alias="reported_at")
    requestText: str = Field(alias="request_text")
