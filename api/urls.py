from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("users.urls")),
    path("", include("companies.urls")),
    path("", include("fishing_bases.urls")),
    path("", include("sessions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
