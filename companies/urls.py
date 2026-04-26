from django.urls import path
from fishing_bases.views import FishingBaseViewSet

from . import views

urlpatterns = [
    path(
        "company/get-info/",
        views.CompanyView.as_view(),
    ),
    path(
        "company/get-fishing-bases/",
        FishingBaseViewSet.as_view({"get": "list"}),
    ),
    path(
        "company/get-staff/",
        views.StaffViewSet.as_view({"get": "list"}),
    ),
    path(
        "company/add-base/",
        FishingBaseViewSet.as_view(
            {"post": "create"},
        ),
    ),
    path(
        "company/add-staff/",
        views.StaffViewSet.as_view({"post": "create"}),
    ),
    path(
        "company/remove-staff/<int:id>/",
        views.StaffViewSet.as_view({"delete": "destroy"}),
    ),
]
