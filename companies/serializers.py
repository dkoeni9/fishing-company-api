from api.models import Company, FishBase, StaffProfile, User
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from fishing_bases.serializers import FishBaseSerializer, SimpleFishBaseSerializer
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ("id", "name", "address")


class CompanyBasesSerializer(serializers.ModelSerializer):
    fish_bases = FishBaseSerializer(source="fishbase_set", many=True, read_only=True)

    class Meta:
        model = Company
        fields = ("id", "name", "address", "fish_bases")


class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    middle_name = serializers.CharField(source="user.middle_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    fish_base = SimpleFishBaseSerializer(read_only=True)

    class Meta:
        model = StaffProfile
        fields = (
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "fish_base",
        )


class StaffCreateSerializer(UserCreateSerializer):
    fish_base_id = serializers.PrimaryKeyRelatedField(
        queryset=FishBase.objects.all(), write_only=True
    )
    description = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = (settings.USER_ID_FIELD, settings.LOGIN_FIELD, "password") + tuple(
            User.REQUIRED_FIELDS
        )
        fields += ("description", "fish_base_id")

    def validate_fish_base_id(self, fish_base):
        user = self.context["request"].user

        if fish_base.company != user.company:
            raise serializers.ValidationError(
                "Fish base does not belong to your company."
            )

        return fish_base

    def validate(self, attrs):
        attrs.pop("fish_base_id", None)
        attrs.pop("description", None)
        return super().validate(attrs)

    def create(self, validated_data):
        fish_base_id = self.initial_data.get("fish_base_id")
        description = self.initial_data.get("description", "")

        user = super().create(validated_data)
        fish_base = FishBase.objects.get(pk=fish_base_id)
        StaffProfile.objects.create(
            user=user, fish_base=fish_base, description=description
        )
        return user
