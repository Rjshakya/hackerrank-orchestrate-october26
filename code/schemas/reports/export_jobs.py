"""Schema for customer_export_jobs_20260914.json.

Top envelope fixed. All 7 export fields required (no nulls observed).
"""

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["ExportJobRecord", "ExportJobs"]


class ExportJobRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    ownerEmail: str = Field(alias="owner_email")
    fileName: str = Field(alias="file_name")
    createdAt: str = Field(alias="created_at")
    expiresAt: str = Field(alias="expires_at")
    downloadAvailable: bool = Field(alias="download_available")
    includedSections: list[str] = Field(alias="included_sections")


class ExportJobs(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    capturedAt: str = Field(alias="captured_at")
    source: str
    collection: str
    records: list[ExportJobRecord] = Field(default_factory=list)
