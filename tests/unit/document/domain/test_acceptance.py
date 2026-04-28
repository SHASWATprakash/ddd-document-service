import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.document.persistence.models import DocumentModel


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def inv001(db):
    return DocumentModel.objects.create(
        reference="INV-001",
        description="Invoice for order",
        document_type="invoice",
        line_item_limit=10,
        line_item_count=5,
    )


@pytest.mark.django_db
class TestCreateDocument:
    def test_create_valid_document_returns_201(self, client):
        response = client.post(
            "/documents",
            {
                "reference": "INV-001",
                "description": "Invoice for order",
                "document_type": "invoice",
                "line_item_limit": 10,
            },
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_with_long_description_returns_error(self, client):
        response = client.post(
            "/documents",
            {
                "reference": "INV-002",
                "description": "This is a description with way too many characters",
                "document_type": "invoice",
                "line_item_limit": 10,
            },
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def test_create_duplicate_reference_returns_error(self, client, inv001):
        response = client.post(
            "/documents",
            {
                "reference": "INV-001",
                "description": "Another invoice",
                "document_type": "invoice",
                "line_item_limit": 5,
            },
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@pytest.mark.django_db
class TestUpdateDocument:
    def test_update_valid_description_returns_200(self, client, inv001):
        response = client.put(
            f"/documents/{inv001.reference}",
            {"description": "Updated invoice description", "line_item_limit": 10},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_long_description_returns_error(self, client, inv001):
        response = client.put(
            f"/documents/{inv001.reference}",
            {
                "description": "Updated with a very long description text",
                "line_item_limit": 10,
            },
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@pytest.mark.django_db
class TestDeleteDocument:
    def test_delete_without_force_with_items_returns_error(self, client, inv001):
        response = client.delete(
            f"/documents/{inv001.reference}",
            {"force_delete": False},
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def test_force_delete_with_items_returns_204(self, client, inv001):
        response = client.delete(
            f"/documents/{inv001.reference}",
            {"force_delete": True},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLineItems:
    def test_add_within_limit_returns_200(self, client, inv001):
        response = client.put(
            f"/documents/{inv001.reference}/line-items",
            {"amount": 3},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_add_exceeding_limit_returns_error(self, client, inv001):
        response = client.put(
            f"/documents/{inv001.reference}/line-items",
            {"amount": 6},
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def test_remove_within_count_returns_200(self, client, inv001):
        response = client.delete(
            f"/documents/{inv001.reference}/line-items",
            {"amount": 5},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_remove_exceeding_count_returns_error(self, client, inv001):
        response = client.delete(
            f"/documents/{inv001.reference}/line-items",
            {"amount": 6},
            format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@pytest.mark.django_db
class TestFindDocument:
    def test_find_existing_document_returns_200(self, client, inv001):
        response = client.get(f"/documents/{inv001.reference}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["reference"] == "INV-001"

    def test_find_nonexistent_document_returns_404(self, client, db):
        response = client.get("/documents/INV-NOTEXIST")
        assert response.status_code == status.HTTP_404_NOT_FOUND