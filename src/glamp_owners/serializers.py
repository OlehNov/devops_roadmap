from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
    ValidationError
)
from rest_framework_simplejwt.tokens import RefreshToken

from glamp_owners.models import GlampOwner
from roles.constants import ProfileStatus, Role
from users.serializers import UserRegisterSerializer, UserSerializer
from users.utils import TokenGenerator

User = get_user_model()


class GlampOwnerRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = GlampOwner
        fields = ["user", "status", "first_name", "last_name", "phone"]
        read_only_fields = ["status"]

    def create(self, validated_data):
        user_data = validated_data.get("user")

        password = user_data.get("password")
        confirm_password = user_data.pop("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                {"password": "Password fields do not match."}
            )

        user = User.objects.create_user(
            email=user_data.pop("email"),
            password=user_data.pop("password"),
            role=Role.OWNER,
            is_active=False,
            is_staff=False,
        )
        return user


class GlampOwnerSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GlampOwner
        fields = "__all__"
        read_only_fields = ["id", "status"]
