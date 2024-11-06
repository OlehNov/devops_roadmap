from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from users.validators import validate_first_name_last_name

from users.utils import TokenGenerator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "email",
            "role",
            "is_active",
            "is_staff",
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
            "first_name",
            "last_name",
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
            "first_name",
            "last_name",
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email" "is_active",
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

        msg = 'Must include "username" and "password".'  # TODO: change username to email
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


class ActivateUserSerializer(serializers.Serializer):
    uuid64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        uuid64 = data.get("uuid64")
        token = data.get("token")
        user_id = force_str(urlsafe_base64_decode(uuid64))
        current_user = get_object_or_404(User, id=user_id)

        if current_user and TokenGenerator().check_token(current_user, token):
            data["current_user"] = current_user
        else:
            raise serializers.ValidationError("Invalid activation data.")

        return data

    def activate(self):
        current_user = self.validated_data["current_user"]

        current_user.is_active = True
        current_user.save()

        refresh = RefreshToken.for_user(current_user)
        return {
            "current_user": current_user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
