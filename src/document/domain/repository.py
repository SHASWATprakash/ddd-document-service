from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from .entities import Document


class DocumentRepository(ABC):
    """Port: abstracts all document persistence operations."""

    @abstractmethod
    def find_by_reference(self, reference: str) -> Optional[Document]:
        raise NotImplementedError

    @abstractmethod
    def save(self, document: Document) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, reference: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists_by_reference(self, reference: str) -> bool:
        raise NotImplementedError