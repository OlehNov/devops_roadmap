from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from users.validators import validate_first_name_last_name
from administrators.models import Administrator
from django.db import transaction
from roles.constants import ProfileStatus, Role
from users.serializers import UserRegisterSerializer, UserSerializer


User = get_user_model()


class AdministratorRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Administrator
        fields = ["user", "status", "first_name", "last_name"]
        read_only_fields = ["id", "status"]

    def validate(self, attrs):
        user_data = attrs.get("user")

        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise ValidationError(
                    {"password": "Password fields do not match."}
                )

        validate_first_name_last_name(attrs.get("first_name"))
        validate_first_name_last_name(attrs.get("last_name"))

        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        user = User.objects.create_user(
            email=user_data.get("email"),
            password=user_data.get("password"),
            role=Role.ADMIN,
            is_active=True,
            is_staff=False,
        )

        Administrator.objects.update(
            first_name=first_name, last_name=last_name
        )

        return Administrator.objects.get(id=user.id, user=user)


class AdministratorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = "__all__"
        read_only_fields = ["id", "status"]

    @transaction.atomic()
    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop("first_name")
        instance.last_name = validated_data.pop("last_name")

        instance.status = ProfileStatus.ACTIVATED
        instance.save()

        return instance
