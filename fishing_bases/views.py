from django.shortcuts import get_object_or_404

from api.models import Fish, FishInFishingBase, FishingBase
from api.permissions import IsEntrepreneur
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
    FishingBaseDetailSerializer,
    FishingBaseFishSerializer,
    FishingBasePhotoSerializer,
    FishingBaseSerializer,
    FishSerializer,
)


class FishingBaseViewSet(viewsets.ModelViewSet):
    serializer_class = FishingBaseSerializer
    permission_classes = [IsEntrepreneur]

    def get_queryset(self):
        user = self.request.user
        return FishingBase.objects.filter(company=user.company).order_by("id")

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class FishingBaseFishViewSet(viewsets.ModelViewSet):
    serializer_class = FishingBaseFishSerializer
    permission_classes = [IsEntrepreneur]

    def get_queryset(self):
        user = self.request.user
        base_id = self.kwargs["base_id"]
        fishing_base = get_object_or_404(FishingBase, pk=base_id)

        if fishing_base.company != user.company:
            raise PermissionDenied("You do not have access to this fishing base.")

        return FishInFishingBase.objects.filter(fishing_base_id=base_id)

    def perform_create(self, serializer):
        user = self.request.user
        base_id = self.kwargs["base_id"]

        try:
            fishing_base = FishingBase.objects.get(id=base_id, company=user.company)
        except FishingBase.DoesNotExist:
            raise PermissionDenied(
                "You are not allowed to add fish to a fishing base that does not belong to your company."
            )

        serializer.save(fishing_base=fishing_base)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        base_id = self.kwargs["base_id"]
        fish_id = self.kwargs["fish_id"]

        try:
            instance = FishInFishingBase.objects.get(
                fishing_base__id=base_id,
                fishing_base__company=user.company,
                fish__id=fish_id,
            )
        except FishInFishingBase.DoesNotExist:
            raise PermissionDenied(
                "You are not allowed to remove fish from a fishing base that does not belong to your company."
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FishListView(generics.ListAPIView):
    queryset = Fish.objects.all()
    serializer_class = FishSerializer
    permission_classes = [IsEntrepreneur]


class UploadPhotoView(views.APIView):
    serializer_class = FishingBasePhotoSerializer
    permission_classes = [IsEntrepreneur]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk, *args, **kwargs):
        user = request.user

        try:
            fishing_base = FishingBase.objects.get(id=pk, company=user.company)
        except FishingBase.DoesNotExist:
            raise PermissionDenied("You do not have access to this fishing base.")

        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.lower().endswith((".png", ".jpg", ".jpeg")):
            return Response(
                {"error": "Invalid file format. Only .png and .jpg are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            instance=fishing_base, data={"photo": file}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Path": fishing_base.photo.url}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchFishingBaseListView(generics.ListAPIView):
    serializer_class = FishingBaseDetailSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "address", "fish__name"]

    def get_queryset(self):
        return FishingBase.objects.all().distinct().order_by("id")
