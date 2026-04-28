from __future__ import annotations

import json

from ..domain.repository import DocumentRepository
from ..domain.value_objects import DocumentDescription, LineItemLimit
from ..persistence.models import OutboxEvent


class UpdateDocumentUseCase:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    def execute(
        self,
        reference: str,
        description: str,
        line_item_limit: int,
    ) -> None:
        document = self._repository.find_by_reference(reference)
        if document is None:
            raise LookupError(f"Document '{reference}' not found.")

        document.update(
            description=DocumentDescription(value=description),
            line_item_limit=LineItemLimit(value=line_item_limit),
        )

        from django.db import transaction

        with transaction.atomic():
            self._repository.save(document)
            for event in document.pull_domain_events():
                OutboxEvent.objects.create(
                    event_id=event.event_id,
                    event_type=type(event).__name__,
                    payload=json.loads(json.dumps(event.__dict__, default=str)),
                )