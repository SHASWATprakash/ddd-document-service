from __future__ import annotations

import json

from ..domain.factory import DocumentFactory
from ..domain.repository import DocumentRepository
from ..domain.services import DocumentUniquenessService
from ..persistence.models import OutboxEvent


class CreateDocumentUseCase:
    def __init__(
        self,
        repository: DocumentRepository,
        uniqueness_service: DocumentUniquenessService,
    ) -> None:
        self._repository = repository
        self._uniqueness_service = uniqueness_service

    def execute(
        self,
        reference: str,
        description: str,
        document_type: str,
        line_item_limit: int,
    ) -> None:
        self._uniqueness_service.assert_reference_is_unique(reference)

        document = DocumentFactory.create(
            reference=reference,
            description=description,
            document_type=document_type,
            line_item_limit=line_item_limit,
        )

        # Transactional outbox: save document + outbox record atomically
        from django.db import transaction

        with transaction.atomic():
            self._repository.save(document)
            for event in document.pull_domain_events():
                OutboxEvent.objects.create(
                    event_id=event.event_id,
                    event_type=type(event).__name__,
                    payload=json.loads(json.dumps(event.__dict__, default=str)),
                )