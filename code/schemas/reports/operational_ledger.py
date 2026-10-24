"""Schemas for 3 operational ledgers with identical shape.

Files: connector_configurations_20260812.json,
customer_export_manifest_20260409.json,
security_audit_ledger_20261001.json.
Top envelope fixed; all 6 claim fields required (no nulls observed).
"""

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["LedgerRecord", "OperationalLedger"]


class LedgerRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    recordedAt: str = Field(alias="recorded_at")
    system: str
    resourceId: str = Field(alias="resource_id")
    recordType: str = Field(alias="record_type")
    result: str
    subjectReference: str = Field(alias="subject_reference")


class OperationalLedger(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exportedAt: str = Field(alias="exported_at")
    origin: str
    recordCount: int = Field(alias="record_count")
    records: list[LedgerRecord] = Field(default_factory=list)
