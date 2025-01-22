from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError

from administrators.models import Administrator
from roles.constants import Role
from users.serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class AdministratorRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Administrator
        fields = ["user", "status", "first_name", "last_name"]
        read_only_fields = ["id", "status"]

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
            role=Role.ADMIN,
            is_active=True,
            is_staff=False,
        )
        return user


class AdministratorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = "__all__"
        read_only_fields = ["id", "status"]
