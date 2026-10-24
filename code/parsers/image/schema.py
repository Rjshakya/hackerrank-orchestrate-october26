"""Structured facts extracted from one evidence screenshot."""

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["ImageFacts"]


class ImageFacts(BaseModel):
    """Typed result of vision extraction. Lists default to empty, scalars required."""

    model_config = ConfigDict(populate_by_name=True)

    fileId: str = Field(alias="file_id")
    systemId: str = Field(alias="system_id")
    capturedAt: str = Field(alias="captured_at")
    subjectRefs: list[str] = Field(default_factory=list, alias="subject_refs")
    resourceIds: list[str] = Field(default_factory=list, alias="resource_ids")
    facts: list[str] = Field(default_factory=list)
    rawText: str = Field(alias="raw_text")
