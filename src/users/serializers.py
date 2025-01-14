from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, Token

from users.utils import TokenGenerator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_deleted",
            "created_at",
            "updated_at",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "confirm_password",
            "is_active",
            "is_staff",
            "role",
        )
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_active",
            "is_staff",
            "role",
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "role",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["password"]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, required=True, allow_blank=False
    )
    password = serializers.CharField(
        max_length=255, write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")

            refresh = RefreshToken.for_user(user)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }

        msg = 'Must include "email" and "password".'
        raise serializers.ValidationError(msg, code="authorization")


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        get_object_or_404(User, email=value)
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password fields didn't match."}
            )

        return attrs

    def save(self):
        password = self.validated_data["new_password"]
        self.user.set_password(password)
        self.user.save()
        return self.user
