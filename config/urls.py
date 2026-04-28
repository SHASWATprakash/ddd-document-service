from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django is running 🚀")


urlpatterns = [
    path("", home),
    path("", include("src.document.infrastructure.controllers.urls")),
]