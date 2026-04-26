from django.urls import path

from . import views

urlpatterns = [
    path(
        "fishing-base/<int:pk>/remove-base/",
        views.FishingBaseViewSet.as_view({"delete": "destroy"}),
    ),
    path(
        "fishing-base/<int:base_id>/get-all-fishes/",
        views.FishingBaseFishViewSet.as_view({"get": "list"}),
    ),
    path(
        "fishing-base/<int:base_id>/add-fish/",
        views.FishingBaseFishViewSet.as_view({"post": "create"}),
    ),
    path(
        "fishing-base/<int:base_id>/remove-fish/<int:fish_id>/",
        views.FishingBaseFishViewSet.as_view({"delete": "destroy"}),
    ),
    path(
        "fishing-base/<int:pk>/upload-photo/",
        views.UploadPhotoView.as_view(),
    ),
    path(
        "fish/get-fishes/",
        views.FishListView.as_view(),
    ),
    path(
        "search/get-fishing-bases/",
        views.SearchFishingBaseListView.as_view(),
    ),
]
