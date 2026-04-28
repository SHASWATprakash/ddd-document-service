from __future__ import annotations

from ..domain.entities import Document
from ..domain.repository import DocumentRepository


class FindDocumentUseCase:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    def execute(self, reference: str) -> Document:
        document = self._repository.find_by_reference(reference)
        if document is None:
            raise LookupError(f"Document '{reference}' not found.")
        return document