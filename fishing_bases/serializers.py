from api.models import Fish, FishBase, FishInBase
from rest_framework import serializers


class FishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fish
        fields = "__all__"


class FishBaseSerializer(serializers.ModelSerializer):
    fish_count = serializers.SerializerMethodField(read_only=True)

    def get_fish_count(self, obj):
        return obj.fish.count()

    class Meta:
        model = FishBase
        fields = (
            "id",
            "name",
            "address",
            "latitude",
            "longitude",
            "description",
            "price_per_hour",
            "entry_price",
            "fish_count",
        )


class SimpleFishBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishBase
        fields = ("id", "name", "address")


class FishBasePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishBase
        fields = ("photo",)


class FBFishesSerializer(serializers.ModelSerializer):
    fish_id = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(source="fish.id", read_only=True)
    name = serializers.CharField(source="fish.name", read_only=True)
    description = serializers.CharField(source="fish.description", read_only=True)

    class Meta:
        model = FishInBase
        fields = ("fish_id", "id", "name", "description", "price_per_kilo")


class FishBaseDetailSerializer(serializers.ModelSerializer):
    fish = FBFishesSerializer(source="fishinbase_set", many=True, read_only=True)

    class Meta:
        model = FishBase
        fields = (
            "id",
            "name",
            "address",
            "latitude",
            "longitude",
            "description",
            "price_per_hour",
            "entry_price",
            "fish",
        )
