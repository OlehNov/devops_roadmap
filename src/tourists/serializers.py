from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError

from roles.constants import ProfileStatus, Role
from tourists.models import Tourist
from users.serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class TouristRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Tourist
        fields = [
            "user",
            "status",
            "first_name",
            "last_name",
            "birthday",
            "phone",
        ]
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
            role=Role.TOURIST,
            is_active=False,
            is_staff=False,
        )
        return user


class TouristSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tourist
        fields = "__all__"
        read_only_fields = ["id", "status"]
