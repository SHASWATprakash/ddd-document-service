from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class DocumentCreated(DomainEvent):
    reference: str = ""
    description: str = ""
    document_type: str = ""
    line_item_limit: int = 0


@dataclass(frozen=True)
class DocumentUpdated(DomainEvent):
    reference: str = ""
    description: str = ""
    line_item_limit: int = 0


@dataclass(frozen=True)
class DocumentDeleted(DomainEvent):
    reference: str = ""