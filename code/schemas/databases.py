"""SQLite snapshot schemas for dataset/evidence/databases.

Python fields use camelCase. Each field aliases to the original
snake_case SQLite column so DB rows load/dump without drift.
All timestamps stay as str to preserve ISO-8601 wire format.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "SnapshotScope",
    "CustomerProfile",
    "CustomerSearchDocument",
    "CustomerAnalyticsProfile",
    "SupportRecord",
    "CustomerExport",
    "ConnectorSubscription",
    "BackupRestoreEntry",
    "SecurityAuditRecord",
    "CustomerInventory",
    "ReplicaRow",
    "CustomerDataPrimary",
    "CustomerDataReadReplica",
    "CustomerDataReplicaApSouth",
    "CustomerDataReplicaEuWest",
    "CustomerDataReportingReplica",
    "CustomerDataFailoverReplica",
    "AccountProfileRow",
    "CustomerProfilesPrimary",
    "CustomerProfilesFailoverReplica",
    "SearchDocumentPrimary",
]


# --- Group A: customer_data_inventory_*.sql (11 files, 9 tables) ---


class SnapshotScope(BaseModel):
    """snapshot_scope(origin_system PK, captured_at NOT NULL)."""

    model_config = ConfigDict(populate_by_name=True)

    originSystem: str = Field(alias="origin_system")
    capturedAt: str = Field(alias="captured_at")


class CustomerProfile(BaseModel):
    """customer_profiles table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    fullName: str | None = Field(default=None, alias="full_name")
    email: str | None = Field(default=None, alias="email")
    phone: str | None = Field(default=None, alias="phone")
    emailHash: str | None = Field(default=None, alias="email_hash")
    accountStatus: str = Field(alias="account_status")
    updatedAt: str = Field(alias="updated_at")


class CustomerSearchDocument(BaseModel):
    """customer_search_documents table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    displayName: str | None = Field(default=None, alias="display_name")
    email: str | None = Field(default=None, alias="email")
    phone: str | None = Field(default=None, alias="phone")
    emailHash: str | None = Field(default=None, alias="email_hash")
    indexName: str = Field(alias="index_name")
    updatedAt: str = Field(alias="updated_at")


class CustomerAnalyticsProfile(BaseModel):
    """customer_analytics_profiles table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    email: str | None = Field(default=None, alias="email")
    phone: str | None = Field(default=None, alias="phone")
    emailHash: str | None = Field(default=None, alias="email_hash")
    audienceCohort: str = Field(alias="audience_cohort")
    updatedAt: str = Field(alias="updated_at")


class SupportRecord(BaseModel):
    """support_records table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    requesterName: str | None = Field(default=None, alias="requester_name")
    requesterEmail: str | None = Field(default=None, alias="requester_email")
    requesterPhone: str | None = Field(default=None, alias="requester_phone")
    messageExcerpt: str = Field(alias="message_excerpt")
    updatedAt: str = Field(alias="updated_at")


class CustomerExport(BaseModel):
    """customer_exports table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    ownerEmail: str | None = Field(default=None, alias="owner_email")
    ownerPhone: str | None = Field(default=None, alias="owner_phone")
    objectKey: str = Field(alias="object_key")
    updatedAt: str = Field(alias="updated_at")


class ConnectorSubscription(BaseModel):
    """connector_subscriptions table; enabled is 0/1 per CHECK."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    customerEmail: str | None = Field(default=None, alias="customer_email")
    connectorName: str = Field(alias="connector_name")
    enabled: Literal[0, 1]
    lastDeliveryStatus: str = Field(alias="last_delivery_status")
    updatedAt: str = Field(alias="updated_at")


class BackupRestoreEntry(BaseModel):
    """backup_restore_entries table; restore_allowed is 0/1 per CHECK."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    customerEmail: str | None = Field(default=None, alias="customer_email")
    archiveKey: str = Field(alias="archive_key")
    restoreAllowed: Literal[0, 1] = Field(alias="restore_allowed")
    updatedAt: str = Field(alias="updated_at")


class SecurityAuditRecord(BaseModel):
    """security_audit_records table in inventory snapshots."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    subjectReference: str = Field(alias="subject_reference")
    eventCode: str = Field(alias="event_code")
    retentionUntil: str = Field(alias="retention_until")
    updatedAt: str = Field(alias="updated_at")


class CustomerInventory(BaseModel):
    """One inventory snapshot file parsed into typed row lists."""

    model_config = ConfigDict(populate_by_name=True)

    snapshotScope: list[SnapshotScope] = Field(
        default_factory=list, alias="snapshot_scope"
    )
    customerProfiles: list[CustomerProfile] = Field(
        default_factory=list, alias="customer_profiles"
    )
    customerSearchDocuments: list[CustomerSearchDocument] = Field(
        default_factory=list, alias="customer_search_documents"
    )
    customerAnalyticsProfiles: list[CustomerAnalyticsProfile] = Field(
        default_factory=list, alias="customer_analytics_profiles"
    )
    supportRecords: list[SupportRecord] = Field(
        default_factory=list, alias="support_records"
    )
    customerExports: list[CustomerExport] = Field(
        default_factory=list, alias="customer_exports"
    )
    connectorSubscriptions: list[ConnectorSubscription] = Field(
        default_factory=list, alias="connector_subscriptions"
    )
    backupRestoreEntries: list[BackupRestoreEntry] = Field(
        default_factory=list, alias="backup_restore_entries"
    )
    securityAuditRecords: list[SecurityAuditRecord] = Field(
        default_factory=list, alias="security_audit_records"
    )


# --- Group B: generic primary/replica shape (11 files) ---


class ReplicaRow(BaseModel):
    """Shared 5-column shape for customer_data_primary and all replicas.

    Covers: customer_data_primary, customer_data_read_replica,
    customer_data_replica_ap_south, customer_data_replica_eu_west,
    customer_data_reporting_replica, customer_data_failover_replica.
    record_json stays as str; callers parse JSON separately so CHECK
    (json_valid(record_json)) semantics are preserved without coercion.
    """

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    originSystem: str = Field(alias="origin_system")
    collectionName: str = Field(alias="collection_name")
    recordJson: str = Field(alias="record_json")
    updatedAt: str = Field(alias="updated_at")


CustomerDataPrimary = ReplicaRow
CustomerDataReadReplica = ReplicaRow
CustomerDataReplicaApSouth = ReplicaRow
CustomerDataReplicaEuWest = ReplicaRow
CustomerDataReportingReplica = ReplicaRow
CustomerDataFailoverReplica = ReplicaRow


# --- Group C: singletons ---


class AccountProfileRow(BaseModel):
    """customer_profiles_primary and customer_profiles_failover_replica."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    userId: str = Field(alias="user_id")
    fullName: str = Field(alias="full_name")
    email: str = Field(alias="email")
    phone: str = Field(alias="phone")
    accountStatus: str = Field(alias="account_status")
    updatedAt: str = Field(alias="updated_at")


CustomerProfilesPrimary = AccountProfileRow
CustomerProfilesFailoverReplica = AccountProfileRow


class SearchDocumentPrimary(BaseModel):
    """search_documents_primary; only resource_id is PK, rest nullable."""

    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    displayName: str | None = Field(default=None, alias="display_name")
    email: str | None = Field(default=None, alias="email")
    sourceResourceId: str | None = Field(default=None, alias="source_resource_id")
    indexedAt: str | None = Field(default=None, alias="indexed_at")
