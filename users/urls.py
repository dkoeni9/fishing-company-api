from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

from . import views

urlpatterns = [
    path("Admin/AddCompany", views.EntrepreneurViewSet.as_view({"post": "create"})),
    path("Auth/SignIn", TokenCreateView.as_view()),
    path("Auth/Logout", TokenDestroyView.as_view()),
    path("Auth/RegisterFisher", views.FisherViewSet.as_view({"post": "create"})),
]
