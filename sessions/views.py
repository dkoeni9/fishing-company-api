from django.shortcuts import get_object_or_404
from django.utils import timezone

from api.models import FishingSession
from api.permissions import IsFisher, IsStaff
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import FisherSessionSerializer, StaffSessionSerializer


class FishingSessionViewSet(viewsets.ViewSet):
    """
    Handles fishing sessions for Fishers (create, list)
    and for Staff (start, close, active_sessions).
    """

    def get_permissions(self):
        if self.action in ["create", "list"]:
            permission_classes = [IsFisher]
        elif self.action in ["start_session", "close_session", "active_sessions"]:
            permission_classes = [IsStaff]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["create", "list"]:
            return FisherSessionSerializer
        return StaffSessionSerializer

    def list(self, request):
        sessions = FishingSession.objects.filter(fisher=request.user)
        serializer = self.get_serializer_class()(sessions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(fisher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def start_session(self, request, pk=None):
        session = get_object_or_404(FishingSession, pk=pk)

        if session.fish_base != request.user.staff_profile.fish_base:
            return Response({"detail": "Not your fish base."}, status=403)

        if session.status != 1:
            return Response(
                {"detail": "Session already started or closed."}, status=400
            )

        session.started_at = timezone.now()
        session.status = 2
        session.staff = request.user
        session.save()

        return Response({"detail": "Session started."})

    @action(detail=True, methods=["post"])
    def close_session(self, request, pk=None):
        session = get_object_or_404(FishingSession, pk=pk)

        if session.fish_base != request.user.staff_profile.fish_base:
            return Response({"detail": "Not your fish base."}, status=403)

        if session.status != 2:
            return Response(
                {"detail": "Only started sessions can be closed."}, status=400
            )

        data = {
            "closed_at": request.data.get("closed_at", timezone.now()),
            "fishes": request.data.get("fishes", []),
            "total_price": request.data.get("total_price", 0),
        }

        serializer = StaffSessionSerializer(
            session, data=data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Session closed."})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["get"])
    def active_sessions(self, request):
        fish_base = request.user.staff_profile.fish_base
        sessions = FishingSession.objects.filter(
            fish_base=fish_base,
            status__in=[FishingSession.Status.CREATED, FishingSession.Status.STARTED],
        )
        serializer = self.get_serializer_class()(sessions, many=True)
        return Response(serializer.data)
