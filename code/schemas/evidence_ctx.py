"""Evidence context for one resource_id.

Collects DB rows, record rows, and raw text snippets that prove the
state of a single resource. fromLogs/fromDocs/fromImg stay as text
because logs are grep-only and docs/images are excerpt strings.
"""

from pydantic import BaseModel, ConfigDict, Field

from .databases import (
    AccountProfileRow,
    BackupRestoreEntry,
    ConnectorSubscription,
    CustomerAnalyticsProfile,
    CustomerExport,
    CustomerProfile,
    CustomerSearchDocument,
    ReplicaRow,
    SearchDocumentPrimary,
    SecurityAuditRecord,
    SupportRecord,
)
from .reports.analytics_report import AnalyticsRecord
from .reports.customer_data_snapshot import SnapshotRecord
from .reports.export_jobs import ExportJobRecord
from .reports.handover import HandoverEntry
from .reports.operational_ledger import LedgerRecord
from .reports.service_resource import (
    AccountProfileLookup,
    AnalyticsProfile,
    BackupRestoreEntryView,
    ConnectorView,
    ExportView,
    SearchIndexQuery,
    SecurityAuditView,
    SupportTicketView,
)

__all__ = ["Source", "FromDb", "FromRecord", "EvidenceCtx"]

DbRow = (
    CustomerProfile
    | CustomerSearchDocument
    | CustomerAnalyticsProfile
    | SupportRecord
    | CustomerExport
    | ConnectorSubscription
    | BackupRestoreEntry
    | SecurityAuditRecord
    | ReplicaRow
    | AccountProfileRow
    | SearchDocumentPrimary
)

RecordRow = (
    SnapshotRecord
    | AccountProfileLookup
    | AnalyticsProfile
    | BackupRestoreEntryView
    | ExportView
    | ConnectorView
    | SearchIndexQuery
    | SecurityAuditView
    | SupportTicketView
    | LedgerRecord
    | AnalyticsRecord
    | ExportJobRecord
    | HandoverEntry
)


class Source(BaseModel):
    """Where one hit came from. All fields required."""

    model_config = ConfigDict(populate_by_name=True)

    evidenceId: str = Field(alias="evidence_id")
    capturedAt: str = Field(alias="captured_at")
    systemId: str = Field(alias="system_id")
    table: str


class FromDb(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: Source
    row: DbRow


class FromRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: Source
    row: RecordRow


class EvidenceCtx(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resourceId: str = Field(alias="resource_id")
    fromDb: list[FromDb] = Field(default_factory=list, alias="from_db")
    fromRecords: list[FromRecord] = Field(default_factory=list, alias="from_records")
    fromLogs: list[str] = Field(default_factory=list, alias="from_logs")
    fromDocs: list[str] = Field(default_factory=list, alias="from_docs")
    fromImg: list[str] = Field(default_factory=list, alias="from_img")
