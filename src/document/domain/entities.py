from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from .events import DocumentCreated, DocumentDeleted, DocumentUpdated, DomainEvent
from .value_objects import DocumentDescription, DocumentReference, LineItemLimit


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"


@dataclass
class Document:
    """Aggregate root for the Document bounded context."""

    reference: DocumentReference
    description: DocumentDescription
    document_type: DocumentType
    line_item_limit: LineItemLimit
    line_item_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    _domain_events: List[DomainEvent] = field(default_factory=list, repr=False)

    # ------------------------------------------------------------------ #
    # Command methods                                                      #
    # ------------------------------------------------------------------ #

    def update(
        self,
        description: DocumentDescription,
        line_item_limit: LineItemLimit,
    ) -> None:
        self.description = description
        self.line_item_limit = line_item_limit
        self._record_event(
            DocumentUpdated(
                event_id=str(uuid.uuid4()),
                reference=str(self.reference),
                description=str(description),
                line_item_limit=line_item_limit.value,
            )
        )

    def add_line_items(self, amount: int) -> None:
        if amount < 1:
            raise ValueError("Amount must be at least 1.")
        projected = self.line_item_count + amount
        if projected > self.line_item_limit.value:
            raise ValueError(
                f"Adding {amount} item(s) would exceed the limit of "
                f"{self.line_item_limit.value}. Current count: {self.line_item_count}."
            )
        self.line_item_count = projected

    def remove_line_items(self, amount: int) -> None:
        if amount < 1:
            raise ValueError("Amount must be at least 1.")
        if amount > self.line_item_count:
            raise ValueError(
                f"Cannot remove {amount} item(s). "
                f"Current count is only {self.line_item_count}."
            )
        self.line_item_count -= amount

    def mark_for_deletion(self, force: bool) -> None:
        if not force and self.line_item_count > 0:
            raise ValueError(
                f"Cannot delete document '{self.reference}' with "
                f"{self.line_item_count} existing line item(s). "
                "Pass force_delete=true to override."
            )
        self._record_event(
            DocumentDeleted(
                event_id=str(uuid.uuid4()),
                reference=str(self.reference),
            )
        )

    # ------------------------------------------------------------------ #
    # Domain event collection                                             #
    # ------------------------------------------------------------------ #

    def _record_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events