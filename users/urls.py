from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView

from . import views

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "fishers/",
        views.FisherViewSet.as_view({"post": "create"}),
    ),
]
