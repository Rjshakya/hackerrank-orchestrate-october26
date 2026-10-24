"""Schema for customer_account_handover_20261001.txt.

Plain-text pipe lines share the 6 claim fields of the JSON ledgers.
All fields required as str; subject may be 'no direct identifier'.
"""

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["HandoverEntry", "Handover"]


class HandoverEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    system: str
    resourceId: str = Field(alias="resource_id")
    recordType: str = Field(alias="record_type")
    result: str
    subject: str

    @classmethod
    def parse_line(cls, line: str) -> "HandoverEntry":
        text = line.strip()
        if text.startswith("- "):
            text = text[2:].strip()
        parts = [p.strip() for p in text.split("|")]
        if len(parts) != 6 or not parts[0].startswith("202"):
            raise ValueError(f"bad handover line: {line!r}")
        observed_at, system, resource_id, record_type, result, subject = parts
        return cls.model_validate(
            {
                "observed_at": observed_at,
                "system": system,
                "resource_id": resource_id,
                "record_type": record_type,
                "result": result,
                "subject": subject,
            }
        )


class Handover(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    snapshot: str
    entries: list[HandoverEntry] = Field(default_factory=list)
