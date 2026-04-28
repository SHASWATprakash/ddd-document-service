from __future__ import annotations

from typing import Optional

from ...domain.entities import Document
from ...domain.repository import DocumentRepository
from ...domain.services import DocumentUniquenessService
from ..mapper import DocumentMapper
from ..models import DocumentModel
from src.document.models import DocumentModel


class DjangoDocumentRepository(DocumentRepository, DocumentUniquenessService):
    """
    Adapter: implements both the repository port and uniqueness service
    using Django ORM backed by PostgreSQL.
    """
    def __init__(self):
        self.model = DocumentModel

    def get_all(self):
        return self.model.objects.all()

    def create(self, data):
        return self.model.objects.create(**data)

    def find_by_reference(self, reference: str) -> Optional[Document]:
        try:
            model = DocumentModel.objects.get(reference=reference)
            return DocumentMapper.to_domain(model)
        except DocumentModel.DoesNotExist:
            return None

    def save(self, document: Document) -> None:
        data = DocumentMapper.to_persistence(document)
        DocumentModel.objects.update_or_create(
            reference=data["reference"],
            defaults={k: v for k, v in data.items() if k != "reference"},
        )

    def delete(self, reference: str) -> None:
        DocumentModel.objects.filter(reference=reference).delete()

    def exists_by_reference(self, reference: str) -> bool:
        return DocumentModel.objects.filter(reference=reference).exists()

    # DocumentUniquenessService
    def is_reference_taken(self, reference: str) -> bool:
        return self.exists_by_reference(reference)
    
    def list_all(self):
     return self.model.objects.all()