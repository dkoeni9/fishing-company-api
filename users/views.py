from django.contrib.auth.models import Group

from api.permissions import IsEntrepreneur
from djoser.views import UserViewSet as DjoserUserViewSet

from .serializers import (
    CustomUserDeleteSerializer,
    EntrepreneurSerializer,
    FisherSerializer,
)


class EntrepreneurViewSet(DjoserUserViewSet):
    def get_permissions(self):
        return [IsEntrepreneur()]

    def get_serializer_class(self):
        if self.action == "create":
            return EntrepreneurSerializer
        if self.action == "destroy":
            return CustomUserDeleteSerializer
        if self.action == "list":
            return EntrepreneurSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer, *args, **kwargs):
        super().perform_create(serializer, *args, **kwargs)
        entrepreneur_group, _ = Group.objects.get_or_create(name="Entrepreneur")
        serializer.instance.groups.add(entrepreneur_group)


class FisherViewSet(DjoserUserViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return FisherSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer, *args, **kwargs):
        super().perform_create(serializer, *args, **kwargs)
        fisher_group, _ = Group.objects.get_or_create(name="Fisher")
        serializer.instance.groups.add(fisher_group)
