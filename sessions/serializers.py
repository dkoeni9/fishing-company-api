from api.models import FishingBase, FishingSession
from fishing_bases.serializers import (
    FishingBaseDetailSerializer,
    FishingBaseFishSerializer,
    SimpleFishingBaseSerializer,
)
from rest_framework import serializers


class FisherSessionSerializer(serializers.ModelSerializer):
    fishing_base_id = serializers.PrimaryKeyRelatedField(
        queryset=FishingBase.objects.all(),
        source="fishing_base",
        write_only=True,
    )
    fishing_base = SimpleFishingBaseSerializer(read_only=True)
    fishes = FishingBaseFishSerializer(
        source="fishing_base.fishinfishingbase_set", many=True, read_only=True
    )

    class Meta:
        model = FishingSession
        fields = (
            "id",
            "status",
            "created_at",
            "started_at",
            "closed_at",
            "total_price",
            "number_of_people",
            "fishing_base_id",
            "fishing_base",
            "fishes",
        )
        read_only_fields = ["started_at", "closed_at", "status", "total_price"]


class StaffSessionSerializer(serializers.ModelSerializer):
    fishing_base = FishingBaseDetailSerializer(read_only=True)

    class Meta:
        model = FishingSession
        fields = (
            "id",
            "status",
            "created_at",
            "started_at",
            "closed_at",
            "total_price",
            "number_of_people",
            "fishing_base",
        )
        read_only_fields = ["created_at", "status"]
