from api.models import FishBase, FishingSession
from fishing_bases.serializers import (
    FBFishesSerializer,
    FishBaseDetailSerializer,
    SimpleFishBaseSerializer,
)
from rest_framework import serializers


class FisherSessionSerializer(serializers.ModelSerializer):
    fish_base_id = serializers.PrimaryKeyRelatedField(
        queryset=FishBase.objects.all(),
        source="fish_base",
        write_only=True,
    )
    fish_base = SimpleFishBaseSerializer(read_only=True)
    fishes = FBFishesSerializer(source="fishinbase_set", many=True, read_only=True)

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
            "fish_base_id",
            "fish_base",
            "fishes",
        )
        read_only_fields = ["started_at", "closed_at", "status", "total_price"]


class StaffSessionSerializer(serializers.ModelSerializer):
    fish_base = FishBaseDetailSerializer(read_only=True)

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
            "fish_base",
        )
        read_only_fields = ["created_at", "status"]
