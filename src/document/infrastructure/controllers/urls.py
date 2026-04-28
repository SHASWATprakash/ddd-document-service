from django.urls import path

from .views import DocumentDetailView, DocumentLineItemsView, DocumentListView

urlpatterns = [
    path("documents", DocumentListView.as_view(), name="document-list"),
    path("documents/<str:reference>", DocumentDetailView.as_view(), name="document-detail"),
    path(
        "documents/<str:reference>/line-items",
        DocumentLineItemsView.as_view(),
        name="document-line-items",
    ),
]