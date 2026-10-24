"""Schema for customer_analytics_report_20260907.json.

Top envelope fixed. user_id / email / phone / email_hash nullable
(1/2 null observed); metrics and recent_activity required.
"""

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AnalyticsMetrics",
    "AnalyticsRecentActivity",
    "AnalyticsRecord",
    "AnalyticsReport",
]


class AnalyticsMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sessions30d: int = Field(alias="sessions_30d")
    productsViewed30d: int = Field(alias="products_viewed_30d")
    ordersCompleted90d: int = Field(alias="orders_completed_90d")
    revenue90dUsd: float = Field(alias="revenue_90d_usd")


class AnalyticsRecentActivity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event: str
    product: str
    quantity: int | None = None


class AnalyticsRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    userId: str | None = Field(default=None, alias="user_id")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")
    reportingWindow: str = Field(alias="reporting_window")
    metrics: AnalyticsMetrics
    recentActivity: list[AnalyticsRecentActivity] = Field(alias="recent_activity")


class AnalyticsReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    capturedAt: str = Field(alias="captured_at")
    source: str
    collection: str
    records: list[AnalyticsRecord] = Field(default_factory=list)
