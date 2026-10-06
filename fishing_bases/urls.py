from django.urls import path

from . import views

urlpatterns = [
    path(
        "fishes/",
        views.FishListView.as_view(),
    ),
    path(
        "fishing-bases/",
        views.SearchFishingBaseListView.as_view(),
    ),
]
