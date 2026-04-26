from api.models import Company, FishingBase, StaffProfile, User
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from fishing_bases.serializers import FishingBaseSerializer, SimpleFishingBaseSerializer
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ("id", "name", "address")


class CompanyBasesSerializer(serializers.ModelSerializer):
    fishing_bases = FishingBaseSerializer(
        source="fishingbase_set", many=True, read_only=True
    )

    class Meta:
        model = Company
        fields = ("id", "name", "address", "fishing_bases")


class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    middle_name = serializers.CharField(source="user.middle_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    fishing_base = SimpleFishingBaseSerializer(read_only=True)

    class Meta:
        model = StaffProfile
        fields = (
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "fishing_base",
        )


class StaffCreateSerializer(UserCreateSerializer):
    fishing_base_id = serializers.PrimaryKeyRelatedField(
        queryset=FishingBase.objects.all(), write_only=True
    )
    description = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = (settings.USER_ID_FIELD, settings.LOGIN_FIELD, "password") + tuple(
            User.REQUIRED_FIELDS
        )
        fields += ("description", "fishing_base_id")

    def validate_fishing_base_id(self, fishing_base):
        user = self.context["request"].user

        if fishing_base.company != user.company:
            raise serializers.ValidationError(
                "Fishing base does not belong to your company."
            )

        return fishing_base

    def validate(self, attrs):
        attrs.pop("fishing_base_id", None)
        attrs.pop("description", None)
        return super().validate(attrs)

    def create(self, validated_data):
        fishing_base_id = self.initial_data.get("fishing_base_id")
        description = self.initial_data.get("description", "")

        user = super().create(validated_data)
        fishing_base = FishingBase.objects.get(pk=fishing_base_id)
        StaffProfile.objects.create(
            user=user, fishing_base=fishing_base, description=description
        )
        return user
