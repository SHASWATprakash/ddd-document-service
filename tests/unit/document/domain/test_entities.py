import pytest
from src.document.domain.entities import Document, DocumentType
from src.document.domain.events import DocumentCreated, DocumentDeleted, DocumentUpdated
from src.document.domain.factory import DocumentFactory
from src.document.domain.value_objects import DocumentDescription, DocumentReference, LineItemLimit


def make_document(line_item_count: int = 0, limit: int = 10) -> Document:
    doc = DocumentFactory.create(
        reference="INV-001",
        description="Invoice for order",
        document_type="invoice",
        line_item_limit=limit,
    )
    doc.line_item_count = line_item_count
    doc.pull_domain_events()  # clear factory events
    return doc


class TestDocumentFactory:
    def test_create_emits_document_created_event(self):
        doc = DocumentFactory.create(
            reference="INV-001",
            description="Invoice for order",
            document_type="invoice",
            line_item_limit=10,
        )
        events = doc.pull_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], DocumentCreated)
        assert events[0].reference == "INV-001"

    def test_invalid_document_type_raises(self):
        with pytest.raises(ValueError):
            DocumentFactory.create(
                reference="INV-001",
                description="Valid",
                document_type="unknown",
                line_item_limit=10,
            )


class TestDocumentAddLineItems:
    def test_add_within_limit_succeeds(self):
        doc = make_document(line_item_count=5, limit=10)
        doc.add_line_items(3)
        assert doc.line_item_count == 8

    def test_add_exceeding_limit_raises(self):
        doc = make_document(line_item_count=5, limit=10)
        with pytest.raises(ValueError, match="exceed the limit"):
            doc.add_line_items(6)


class TestDocumentRemoveLineItems:
    def test_remove_within_count_succeeds(self):
        doc = make_document(line_item_count=5)
        doc.remove_line_items(5)
        assert doc.line_item_count == 0

    def test_remove_exceeding_count_raises(self):
        doc = make_document(line_item_count=5)
        with pytest.raises(ValueError, match="Cannot remove"):
            doc.remove_line_items(6)


class TestDocumentDelete:
    def test_force_delete_with_items_succeeds(self):
        doc = make_document(line_item_count=5)
        doc.mark_for_deletion(force=True)
        events = doc.pull_domain_events()
        assert any(isinstance(e, DocumentDeleted) for e in events)

    def test_non_force_delete_with_items_raises(self):
        doc = make_document(line_item_count=5)
        with pytest.raises(ValueError, match="force_delete=true"):
            doc.mark_for_deletion(force=False)

    def test_non_force_delete_without_items_succeeds(self):
        doc = make_document(line_item_count=0)
        doc.mark_for_deletion(force=False)
        events = doc.pull_domain_events()
        assert any(isinstance(e, DocumentDeleted) for e in events)


class TestDocumentUpdate:
    def test_update_emits_updated_event(self):
        doc = make_document()
        doc.update(
            description=DocumentDescription(value="Updated invoice description"),
            line_item_limit=LineItemLimit(value=20),
        )
        events = doc.pull_domain_events()
        assert any(isinstance(e, DocumentUpdated) for e in events)