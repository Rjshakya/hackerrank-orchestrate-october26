"""User identity context from dataset/user_identities.csv."""

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["UserCtx"]


class UserCtx(BaseModel):
    """Current identity snapshot. All 6 fields required (0 nulls in 850 rows)."""

    model_config = ConfigDict(populate_by_name=True)

    userId: str = Field(alias="user_id")
    name: str
    email: str
    phone: str
    emailHash: str = Field(alias="email_hash")
    updatedAt: str = Field(alias="updated_at")
