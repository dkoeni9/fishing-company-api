from django.urls import path

from .views import CompanyView, StaffViewSet
from fishing_bases.views import (
    FishingBaseFishViewSet,
    FishingBaseViewSet,
    UploadPhotoView,
)
from users.views import EntrepreneurViewSet

urlpatterns = [
    path(
        "companies/",
        EntrepreneurViewSet.as_view({"post": "create"}),
    ),
    path(
        "companies/me/",
        CompanyView.as_view(),
    ),
    path(
        "companies/me/fishing-bases/",
        FishingBaseViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "companies/me/fishing-bases/<int:pk>/",
        FishingBaseViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
    ),
    path(
        "companies/me/fishing-bases/<int:base_id>/fishes/",
        FishingBaseFishViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "companies/me/fishing-bases/<int:base_id>/fishes/<int:fish_id>/",
        FishingBaseFishViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
    ),
    path(
        "companies/me/fishing-bases/<int:pk>/photo/",
        UploadPhotoView.as_view(),
    ),
    path(
        "companies/me/staff/",
        StaffViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "companies/me/staff/<int:id>/",
        StaffViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
    ),
]
