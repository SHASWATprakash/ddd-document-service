from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentDescription:
    """Value object encapsulating description validation rules."""

    value: str

    MAX_LENGTH = 30

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Description cannot be empty.")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(
                f"Description cannot exceed {self.MAX_LENGTH} characters. "
                f"Got {len(self.value)}."
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class DocumentReference:
    """Value object for the unique document reference."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Reference cannot be empty.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class LineItemLimit:
    """Value object ensuring line item limit is a positive integer."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("Line item limit must be at least 1.")