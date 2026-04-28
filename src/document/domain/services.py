from __future__ import annotations

from abc import ABC, abstractmethod


class DocumentUniquenessService(ABC):
    """
    Domain Service: enforces uniqueness of document references.
    Abstractions live in the domain; implementations in persistence.
    """

    @abstractmethod
    def is_reference_taken(self, reference: str) -> bool:
        raise NotImplementedError

    def assert_reference_is_unique(self, reference: str) -> None:
        if self.is_reference_taken(reference):
            raise ValueError(
                f"A document with reference '{reference}' already exists."
            )