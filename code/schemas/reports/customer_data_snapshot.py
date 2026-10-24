"""Schemas for customer_data_snapshot_bundle_*.json (12 files).

Envelope is fixed across all bundles. Record shape varies by
(data_store, collection); 14 variants share only resource_id.
Strict per-collection models carry exact required/optional types.
SnapshotRecord is the unified nullable view for generic parsing.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "SnapshotMetrics",
    "SnapshotRecentActivity",
    "SnapshotSearchDocumentPayload",
    "SnapshotAccountProfile",
    "SnapshotAnalyticsReport",
    "SnapshotBackupCatalog",
    "SnapshotExportJob",
    "SnapshotConnector",
    "SnapshotSearchDocument",
    "SnapshotAuditEvent",
    "SnapshotSupportConversation",
    "SnapshotTicketAttachment",
    "SnapshotLegalHold",
    "SnapshotTombstone",
    "SnapshotOperationalHistory",
    "SnapshotRecord",
    "Snapshot",
    "CustomerDataSnapshotBundle",
]


class SnapshotMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sessions30d: int = Field(alias="sessions_30d")
    productsViewed30d: int = Field(alias="products_viewed_30d")
    ordersCompleted90d: int = Field(alias="orders_completed_90d")
    revenue90dUsd: float = Field(alias="revenue_90d_usd")


class SnapshotRecentActivity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event: str
    product: str
    quantity: int | None = None


class SnapshotSearchDocumentPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    displayName: str | None = Field(default=None, alias="display_name")
    email: str | None = None
    customerReference: str | None = Field(default=None, alias="customer_reference")


class SnapshotAccountProfile(BaseModel):
    """account_service / customer_profiles. No nulls observed."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str = Field(alias="customer_reference")
    fullName: str = Field(alias="full_name")
    email: str
    phone: str
    accountStatus: str = Field(alias="account_status")
    signupChannel: str = Field(alias="signup_channel")


class SnapshotAnalyticsReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    userId: str | None = Field(default=None, alias="user_id")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")
    reportingWindow: str = Field(alias="reporting_window")
    metrics: SnapshotMetrics
    recentActivity: list[SnapshotRecentActivity] = Field(alias="recent_activity")


class SnapshotBackupCatalog(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    archivePath: str = Field(alias="archive_path")
    subjectReference: str = Field(alias="subject_reference")
    restoreAllowed: bool = Field(alias="restore_allowed")
    encryption: str


class SnapshotExportJob(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    ownerEmail: str = Field(alias="owner_email")
    fileName: str = Field(alias="file_name")
    createdAt: str = Field(alias="created_at")
    expiresAt: str = Field(alias="expires_at")
    downloadAvailable: bool = Field(alias="download_available")
    includedSections: list[str] = Field(alias="included_sections")


class SnapshotConnector(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    connectorName: str = Field(alias="connector_name")
    subjectSelector: str = Field(alias="subject_selector")
    destination: str
    enabled: bool
    mode: str


class SnapshotSearchDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    indexName: str = Field(alias="index_name")
    document: SnapshotSearchDocumentPayload


class SnapshotAuditEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    subjectReference: str = Field(alias="subject_reference")
    eventName: str = Field(alias="event_name")
    actorType: str = Field(alias="actor_type")
    integritySeal: str = Field(alias="integrity_seal")


class SnapshotSupportConversation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    ticketId: str = Field(alias="ticket_id")
    subjectReference: str = Field(alias="subject_reference")
    channel: str
    messageText: str = Field(alias="message_text")


class SnapshotTicketAttachment(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    ticketId: str = Field(alias="ticket_id")
    fileName: str = Field(alias="file_name")
    uploadedBy: str = Field(alias="uploaded_by")
    storageClass: str = Field(alias="storage_class")


class SnapshotLegalHold(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    subjectReference: str = Field(alias="subject_reference")
    orderReference: str = Field(alias="order_reference")
    retentionReason: str = Field(alias="retention_reason")
    retainedUntil: str = Field(alias="retained_until")


class SnapshotTombstone(BaseModel):
    """identity_service / deleted_customer_references."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    subjectReference: str = Field(alias="subject_reference")
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")
    accountStatus: str = Field(alias="account_status")


class SnapshotOperationalHistory(BaseModel):
    """operational_record_history for 3 data_stores."""

    model_config = ConfigDict(populate_by_name=True)

    recordedAt: str = Field(alias="recorded_at")
    system: str
    resourceId: str = Field(alias="resource_id")
    recordType: str = Field(alias="record_type")
    result: str
    lookupValue: str = Field(alias="lookup_value")


class SnapshotRecord(BaseModel):
    """Unified nullable view: only resource_id is common to all 14 variants."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    fullName: str | None = Field(default=None, alias="full_name")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")
    accountStatus: str | None = Field(default=None, alias="account_status")
    signupChannel: str | None = Field(default=None, alias="signup_channel")
    userId: str | None = Field(default=None, alias="user_id")
    reportingWindow: str | None = Field(default=None, alias="reporting_window")
    metrics: SnapshotMetrics | None = None
    recentActivity: list[SnapshotRecentActivity] | None = Field(
        default=None, alias="recent_activity"
    )
    archivePath: str | None = Field(default=None, alias="archive_path")
    subjectReference: str | None = Field(default=None, alias="subject_reference")
    restoreAllowed: bool | None = Field(default=None, alias="restore_allowed")
    encryption: str | None = None
    ownerEmail: str | None = Field(default=None, alias="owner_email")
    fileName: str | None = Field(default=None, alias="file_name")
    createdAt: str | None = Field(default=None, alias="created_at")
    expiresAt: str | None = Field(default=None, alias="expires_at")
    downloadAvailable: bool | None = Field(default=None, alias="download_available")
    includedSections: list[str] | None = Field(default=None, alias="included_sections")
    connectorName: str | None = Field(default=None, alias="connector_name")
    subjectSelector: str | None = Field(default=None, alias="subject_selector")
    destination: str | None = None
    enabled: bool | None = None
    mode: str | None = None
    indexName: str | None = Field(default=None, alias="index_name")
    document: SnapshotSearchDocumentPayload | None = None
    eventName: str | None = Field(default=None, alias="event_name")
    actorType: str | None = Field(default=None, alias="actor_type")
    integritySeal: str | None = Field(default=None, alias="integrity_seal")
    ticketId: str | None = Field(default=None, alias="ticket_id")
    channel: str | None = None
    messageText: str | None = Field(default=None, alias="message_text")
    storageClass: str | None = Field(default=None, alias="storage_class")
    uploadedBy: str | None = Field(default=None, alias="uploaded_by")
    orderReference: str | None = Field(default=None, alias="order_reference")
    retentionReason: str | None = Field(default=None, alias="retention_reason")
    retainedUntil: str | None = Field(default=None, alias="retained_until")
    name: str | None = None
    recordedAt: str | None = Field(default=None, alias="recorded_at")
    system: str | None = None
    recordType: str | None = Field(default=None, alias="record_type")
    result: str | None = None
    lookupValue: str | None = Field(default=None, alias="lookup_value")


class Snapshot(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    capturedAt: str = Field(alias="captured_at")
    dataStore: str = Field(alias="data_store")
    collection: str
    records: list[SnapshotRecord] = Field(default_factory=list)


class CustomerDataSnapshotBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exportedAt: str = Field(alias="exported_at")
    source: str
    snapshots: list[Snapshot] = Field(default_factory=list)

    _source: Literal["records_assurance_service"] = "records_assurance_service"
