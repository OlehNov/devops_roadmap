from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField,
)
from users.validators import validate_first_name_last_name
from managers.models import GlampManager
from django.db import transaction
from roles.constants import ProfileStatus, Role
from users.serializers import UserRegisterSerializer, UserSerializer


User = get_user_model()


class ManagerRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = GlampManager
        fields = ["user", "status"]
        read_only_fields = ["status"]

    def validate(self, attrs):
        user_data = attrs.get("user")

        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError(
                    {"password": "Password fields do not match."}
                )

        validate_first_name_last_name(user_data.get("first_name"))
        validate_first_name_last_name(user_data.get("last_name"))

        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            password=user_data.get("password"),
            role=Role.MANAGER,
            is_active=True,
            is_staff=True,
        )

        manager, _ = GlampManager.objects.get_or_create(
            id=user.id,
            email=user.email,
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            status=ProfileStatus.ACTIVATED,
        )

        return manager


class ManagerSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GlampManager
        fields = ["user", "status"]
        read_only_fields = ["status"]

    @transaction.atomic()
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        user = instance.user

        if user_data:
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.save()

        instance.id = user.id
        instance.first_name = user.first_name
        instance.last_name = user.last_name
        instance.status = ProfileStatus.ACTIVATED
        instance.save()

        return instance
