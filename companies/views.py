from django.contrib.auth.models import Group

from api.models import FishingBase, FishingBaseStaff
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
        fishing_base_ids = FishingBase.objects.filter(company=user.company).values_list(
            "id", flat=True
        )

        return (
            FishingBaseStaff.objects.filter(fishing_base_id__in=fishing_base_ids)
            .select_related("user", "fishing_base")
            .order_by("fishing_base_id")
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
        fishing_base_staff = self.get_object()
        user = fishing_base_staff.user

        try:
            staff_group = Group.objects.get(name="Staff")
            user.groups.remove(staff_group)
        except Group.DoesNotExist:
            pass

        user.is_active = False
        user.save()
        fishing_base_staff.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
