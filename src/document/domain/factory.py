from __future__ import annotations

import uuid

from .entities import Document, DocumentType
from .events import DocumentCreated
from .value_objects import DocumentDescription, DocumentReference, LineItemLimit


class DocumentFactory:
    """Responsible for constructing valid Document aggregates."""

    @staticmethod
    def create(
        reference: str,
        description: str,
        document_type: str,
        line_item_limit: int,
    ) -> Document:
        ref = DocumentReference(value=reference)
        desc = DocumentDescription(value=description)
        doc_type = DocumentType(document_type)
        limit = LineItemLimit(value=line_item_limit)

        document = Document(
            reference=ref,
            description=desc,
            document_type=doc_type,
            line_item_limit=limit,
        )

        document._record_event(
            DocumentCreated(
                event_id=str(uuid.uuid4()),
                reference=reference,
                description=description,
                document_type=document_type,
                line_item_limit=line_item_limit,
            )
        )

        return document