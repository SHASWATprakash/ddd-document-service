import pytest
from src.document.domain.value_objects import (
    DocumentDescription,
    DocumentReference,
    LineItemLimit,
)


class TestDocumentDescription:
    def test_valid_description_is_accepted(self):
        desc = DocumentDescription(value="Invoice for order")
        assert str(desc) == "Invoice for order"

    def test_description_at_exact_limit_is_accepted(self):
        desc = DocumentDescription(value="A" * 30)
        assert len(str(desc)) == 30

    def test_description_exceeding_limit_raises(self):
        with pytest.raises(ValueError, match="cannot exceed 30 characters"):
            DocumentDescription(value="This is a description with way too many characters")

    def test_empty_description_raises(self):
        with pytest.raises(ValueError):
            DocumentDescription(value="")


class TestDocumentReference:
    def test_valid_reference_is_accepted(self):
        ref = DocumentReference(value="INV-001")
        assert str(ref) == "INV-001"

    def test_empty_reference_raises(self):
        with pytest.raises(ValueError):
            DocumentReference(value="")


class TestLineItemLimit:
    def test_valid_limit_is_accepted(self):
        limit = LineItemLimit(value=10)
        assert limit.value == 10

    def test_zero_limit_raises(self):
        with pytest.raises(ValueError):
            LineItemLimit(value=0)