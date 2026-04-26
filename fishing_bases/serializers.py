from api.models import Fish, FishInFishingBase, FishingBase
from rest_framework import serializers


class FishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fish
        fields = "__all__"


class FishingBaseSerializer(serializers.ModelSerializer):
    fish_count = serializers.SerializerMethodField(read_only=True)

    def get_fish_count(self, obj):
        return obj.fish.count()

    class Meta:
        model = FishingBase
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


class SimpleFishingBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishingBase
        fields = ("id", "name", "address")


class FishingBasePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishingBase
        fields = ("photo",)


class FishingBaseFishSerializer(serializers.ModelSerializer):
    fish_id = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(source="fish.id", read_only=True)
    name = serializers.CharField(source="fish.name", read_only=True)
    description = serializers.CharField(source="fish.description", read_only=True)

    class Meta:
        model = FishInFishingBase
        fields = ("fish_id", "id", "name", "description", "price_per_kilo")


class FishingBaseDetailSerializer(serializers.ModelSerializer):
    fish = FishingBaseFishSerializer(
        source="fishinfishingbase_set", many=True, read_only=True
    )

    class Meta:
        model = FishingBase
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
