from django.urls import path

from . import views

urlpatterns = [
    path(
        "session/me/",
        views.FishingSessionViewSet.as_view({"get": "list"}),
    ),
    path(
        "session/",
        views.FishingSessionViewSet.as_view({"post": "create"}),
    ),
    path(
        "session/staff/",
        views.FishingSessionViewSet.as_view({"get": "active_sessions"}),
    ),
    path(
        "session/<int:pk>/start/",
        views.FishingSessionViewSet.as_view({"post": "start_session"}),
    ),
    path(
        "session/<int:pk>/close/",
        views.FishingSessionViewSet.as_view({"post": "close_session"}),
    ),
]
