from django.urls import path

from . import views

urlpatterns = [
    path(
        "session/get-your-session/",
        views.FishingSessionViewSet.as_view({"get": "list"}),
    ),
    path(
        "session/create-session/",
        views.FishingSessionViewSet.as_view({"post": "create"}),
    ),
    path(
        "session/get-staff-session/",
        views.FishingSessionViewSet.as_view({"get": "active_sessions"}),
    ),
    path(
        "session/start-session/<int:pk>/",
        views.FishingSessionViewSet.as_view({"post": "start_session"}),
    ),
    path(
        "session/close-session/<int:pk>/",
        views.FishingSessionViewSet.as_view({"post": "close_session"}),
    ),
]
