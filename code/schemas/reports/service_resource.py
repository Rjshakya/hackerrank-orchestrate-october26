"""Schemas for service_resource_export_*.json (11 files).

Top envelope is fixed. service_exports maps each service name to an
object holding its list (e.g. account_service -> {profile_lookups: []}).
Service objects are optional because backup/export are absent in files.
Within each list, only fields never observed as null are required.
"""

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AccountProfilePayload",
    "AccountProfileLookup",
    "AccountServiceExports",
    "AnalyticsProfile",
    "AnalyticsServiceExports",
    "BackupRestoreEntryView",
    "BackupServiceExports",
    "ExportView",
    "ExportServiceExports",
    "ConnectorView",
    "IntegrationServiceExports",
    "SearchHitDocument",
    "SearchHits",
    "SearchIndexQuery",
    "SearchServiceExports",
    "SecurityAuditView",
    "SecurityServiceExports",
    "SupportTicketView",
    "SupportServiceExports",
    "ServiceExports",
    "ServiceResourceExport",
]


class AccountProfilePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    customerReference: str | None = Field(default=None, alias="customer_reference")
    fullName: str | None = Field(default=None, alias="full_name")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")


class AccountProfileLookup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    statusCode: int = Field(alias="status_code")
    profile: AccountProfilePayload | None = None


class AccountServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    profileLookups: list[AccountProfileLookup] = Field(
        default_factory=list, alias="profile_lookups"
    )


class AnalyticsProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")
    audienceCohort: str = Field(alias="audience_cohort")


class AnalyticsServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    profiles: list[AnalyticsProfile] = Field(default_factory=list)


class BackupRestoreEntryView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    customerEmail: str | None = Field(default=None, alias="customer_email")
    archiveKey: str = Field(alias="archive_key")
    restoreAllowed: bool = Field(alias="restore_allowed")


class BackupServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    restoreEntries: list[BackupRestoreEntryView] = Field(
        default_factory=list, alias="restore_entries"
    )


class ExportView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    ownerEmail: str = Field(alias="owner_email")
    ownerPhone: str | None = Field(default=None, alias="owner_phone")
    objectKey: str = Field(alias="object_key")


class ExportServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exports: list[ExportView] = Field(default_factory=list)


class ConnectorView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    customerEmail: str | None = Field(default=None, alias="customer_email")
    connectorName: str = Field(alias="connector_name")
    enabled: bool
    lastDeliveryStatus: str = Field(alias="last_delivery_status")


class IntegrationServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    connectors: list[ConnectorView] = Field(default_factory=list)


class SearchHitDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    displayName: str | None = Field(default=None, alias="display_name")
    email: str | None = None
    phone: str | None = None
    emailHash: str | None = Field(default=None, alias="email_hash")


class SearchHits(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: int
    documents: list[SearchHitDocument] = Field(default_factory=list)


class SearchIndexQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    query: str
    hits: SearchHits


class SearchServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    indexQueries: list[SearchIndexQuery] = Field(
        default_factory=list, alias="index_queries"
    )


class SecurityAuditView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    subjectReference: str = Field(alias="subject_reference")
    eventCode: str = Field(alias="event_code")
    retentionUntil: str = Field(alias="retention_until")


class SecurityServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auditRecords: list[SecurityAuditView] = Field(
        default_factory=list, alias="audit_records"
    )


class SupportTicketView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    observedAt: str = Field(alias="observed_at")
    resourceId: str = Field(alias="resource_id")
    customerReference: str | None = Field(default=None, alias="customer_reference")
    requesterName: str | None = Field(default=None, alias="requester_name")
    requesterEmail: str | None = Field(default=None, alias="requester_email")
    requesterPhone: str | None = Field(default=None, alias="requester_phone")
    messageExcerpt: str = Field(alias="message_excerpt")


class SupportServiceExports(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tickets: list[SupportTicketView] = Field(default_factory=list)


class ServiceExports(BaseModel):
    """Service objects nullable because files omit some services."""

    model_config = ConfigDict(populate_by_name=True)

    accountService: AccountServiceExports | None = Field(
        default=None, alias="account_service"
    )
    analyticsPlatform: AnalyticsServiceExports | None = Field(
        default=None, alias="analytics_platform"
    )
    backupService: BackupServiceExports | None = Field(
        default=None, alias="backup_service"
    )
    exportService: ExportServiceExports | None = Field(
        default=None, alias="export_service"
    )
    integrationService: IntegrationServiceExports | None = Field(
        default=None, alias="integration_service"
    )
    searchService: SearchServiceExports | None = Field(
        default=None, alias="search_service"
    )
    securityService: SecurityServiceExports | None = Field(
        default=None, alias="security_service"
    )
    supportPlatform: SupportServiceExports | None = Field(
        default=None, alias="support_platform"
    )


class ServiceResourceExport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    exportedAt: str = Field(alias="exported_at")
    region: str
    source: str
    serviceExports: ServiceExports = Field(alias="service_exports")
