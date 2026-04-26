from django.contrib.auth.models import Group

from api.models import Company, User
from companies.serializers import CompanySerializer
from djoser.conf import settings
from djoser.serializers import TokenSerializer, UserCreateSerializer, UserDeleteSerializer
from rest_framework import serializers


class EntrepreneurSerializer(UserCreateSerializer):
    company = CompanySerializer()

    class Meta:
        model = User
        fields = (settings.USER_ID_FIELD, settings.LOGIN_FIELD, "password") + tuple(
            User.REQUIRED_FIELDS
        )
        fields += ("company",)

    def create(self, validated_data):
        company_data = validated_data.pop("company")
        user = User.objects.create(**validated_data)
        Company.objects.create(owner=user, **company_data)
        return user


class FisherSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (settings.USER_ID_FIELD, settings.LOGIN_FIELD, "password") + tuple(
            User.REQUIRED_FIELDS
        )


class CustomUserDeleteSerializer(UserDeleteSerializer):
    class Meta:
        model = User
        fields = []


class CustomTokenSerializer(TokenSerializer):
    token = serializers.CharField(source="key")
    id = serializers.IntegerField(source="user.pk")
    username = serializers.CharField(source="user.username")
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}".strip()

    def get_role(self, obj):
        user = obj.user
        group = user.groups.first()
        return group.name if group else None

    class Meta(TokenSerializer.Meta):
        fields = ("id", "username", "full_name", "role", "token")
