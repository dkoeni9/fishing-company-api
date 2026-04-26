from django.contrib.auth.models import Group

from api.models import FishBase, StaffProfile
from api.permissions import IsEntrepreneur
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import CompanySerializer, StaffCreateSerializer, StaffSerializer
from users.serializers import CustomUserDeleteSerializer


class CompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsEntrepreneur]

    def get_object(self):
        return self.request.user.company


class StaffViewSet(DjoserUserViewSet):
    def get_permissions(self):
        return [IsEntrepreneur()]

    def get_queryset(self):
        user = self.request.user
        fish_base_ids = FishBase.objects.filter(company=user.company).values_list(
            "id", flat=True
        )

        return (
            StaffProfile.objects.filter(fish_base_id__in=fish_base_ids)
            .select_related("user", "fish_base")
            .order_by("fish_base_id")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return StaffCreateSerializer
        if self.action == "destroy":
            return CustomUserDeleteSerializer
        if self.action == "list":
            return StaffSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer, *args, **kwargs):
        super().perform_create(serializer, *args, **kwargs)
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        serializer.instance.groups.add(staff_group)

    def destroy(self, request, *args, **kwargs):
        staff_profile = self.get_object()
        user = staff_profile.user

        try:
            staff_group = Group.objects.get(name="Staff")
            user.groups.remove(staff_group)
        except Group.DoesNotExist:
            pass

        user.is_active = False
        user.save()
        staff_profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
