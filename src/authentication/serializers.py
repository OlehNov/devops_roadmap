from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer, CharField
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["password"] = user.password

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional data or modify the response data
        data["result"] = "Token has been refreshed successfully"

        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional logic or custom response data
        data["result"] = "Token is valid"

        return data


class UserLogoutSerializer(Serializer):
    refresh_token = CharField()
