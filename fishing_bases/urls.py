from django.urls import path

from . import views

urlpatterns = [
    path(
        "fishbase/<int:pk>/remove-base/",
        views.FishBaseViewSet.as_view({"delete": "destroy"}),
    ),
    path(
        "fishbase/<int:base_id>/get-all-fishes/",
        views.FBFishesViewSet.as_view({"get": "list"}),
    ),
    path(
        "fishbase/<int:base_id>/add-fish/",
        views.FBFishesViewSet.as_view({"post": "create"}),
    ),
    path(
        "fishbase/<int:base_id>/remove-fish/<int:fish_id>/",
        views.FBFishesViewSet.as_view({"delete": "destroy"}),
    ),
    path(
        "fishbase/<int:pk>/upload-photo/",
        views.UploadPhotoView.as_view(),
    ),
    path(
        "fish/get-fishes/",
        views.FishListView.as_view(),
    ),
    path(
        "search/get-fishbases/",
        views.SearchFishBaseListView.as_view(),
    ),
]
