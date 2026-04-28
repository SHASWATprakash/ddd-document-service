from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ...domain.entities import Document
from ...persistence.repository.document_repository import DjangoDocumentRepository
from ...use_cases.add_line_item import AddLineItemUseCase
from ...use_cases.create_document import CreateDocumentUseCase
from ...use_cases.delete_document import DeleteDocumentUseCase
from ...use_cases.find_document import FindDocumentUseCase
from ...use_cases.remove_line_item import RemoveLineItemUseCase
from ...use_cases.update_document import UpdateDocumentUseCase
from .serializers import (
    CreateDocumentSerializer,
    DeleteDocumentSerializer,
    LineItemSerializer,
    UpdateDocumentSerializer,
)


def _serialize_document(document: Document) -> dict:
    return {
        "reference": str(document.reference),
        "description": str(document.description),
        "document_type": document.document_type.value,
        "line_item_count": document.line_item_count,
        "line_item_limit": document.line_item_limit.value,
        "created_at": document.created_at.isoformat() if document.created_at else None,
    }


def _get_repository() -> DjangoDocumentRepository:
    return DjangoDocumentRepository()


class DocumentListView(APIView):
    def post(self, request: Request) -> Response:
        serializer = CreateDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _get_repository()
        use_case = CreateDocumentUseCase(
            repository=repo,
            uniqueness_service=repo,
        )

        use_case.execute(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class DocumentDetailView(APIView):
    def get(self, request: Request, reference: str) -> Response:
        repo = _get_repository()
        use_case = FindDocumentUseCase(repository=repo)
        document = use_case.execute(reference)
        return Response(_serialize_document(document), status=status.HTTP_200_OK)

    def put(self, request: Request, reference: str) -> Response:
        serializer = UpdateDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _get_repository()
        use_case = UpdateDocumentUseCase(repository=repo)
        use_case.execute(reference=reference, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, reference: str) -> Response:
        serializer = DeleteDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _get_repository()
        use_case = DeleteDocumentUseCase(repository=repo)
        use_case.execute(
            reference=reference,
            force_delete=serializer.validated_data["force_delete"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentLineItemsView(APIView):
    def put(self, request: Request, reference: str) -> Response:
        serializer = LineItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _get_repository()
        use_case = AddLineItemUseCase(repository=repo)
        use_case.execute(reference=reference, amount=serializer.validated_data["amount"])
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, reference: str) -> Response:
        serializer = LineItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _get_repository()
        use_case = RemoveLineItemUseCase(repository=repo)
        use_case.execute(reference=reference, amount=serializer.validated_data["amount"])
        return Response(status=status.HTTP_200_OK)