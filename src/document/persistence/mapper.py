from __future__ import annotations

from ..domain.entities import Document, DocumentType
from ..domain.value_objects import DocumentDescription, DocumentReference, LineItemLimit
from .models import DocumentModel


class DocumentMapper:
    """Translates between DocumentModel (ORM) and Document (domain entity)."""

    @staticmethod
    def to_domain(model: DocumentModel) -> Document:
        return Document(
            reference=DocumentReference(value=model.reference),
            description=DocumentDescription(value=model.description),
            document_type=DocumentType(model.document_type),
            line_item_limit=LineItemLimit(value=model.line_item_limit),
            line_item_count=model.line_item_count,
            created_at=model.created_at,
        )

    @staticmethod
    def to_persistence(document: Document) -> dict:
        return {
            "reference": str(document.reference),
            "description": str(document.description),
            "document_type": document.document_type.value,
            "line_item_limit": document.line_item_limit.value,
            "line_item_count": document.line_item_count,
        }