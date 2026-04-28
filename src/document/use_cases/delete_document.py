from __future__ import annotations

import json

from ..domain.repository import DocumentRepository
from ..persistence.models import OutboxEvent


class DeleteDocumentUseCase:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    def execute(self, reference: str, force_delete: bool) -> None:
        document = self._repository.find_by_reference(reference)
        if document is None:
            raise LookupError(f"Document '{reference}' not found.")

        document.mark_for_deletion(force=force_delete)

        from django.db import transaction

        with transaction.atomic():
            self._repository.delete(reference)
            for event in document.pull_domain_events():
                OutboxEvent.objects.create(
                    event_id=event.event_id,
                    event_type=type(event).__name__,
                    payload=json.loads(json.dumps(event.__dict__, default=str)),
                )