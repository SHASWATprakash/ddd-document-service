from __future__ import annotations

from ..domain.repository import DocumentRepository


class RemoveLineItemUseCase:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    def execute(self, reference: str, amount: int) -> None:
        document = self._repository.find_by_reference(reference)
        if document is None:
            raise LookupError(f"Document '{reference}' not found.")

        document.remove_line_items(amount)
        self._repository.save(document)