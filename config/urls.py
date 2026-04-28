from django.urls import path, include

urlpatterns = [
    path("", include("src.document.infrastructure.controllers.urls")),
]