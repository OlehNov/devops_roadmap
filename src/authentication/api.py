from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema

from authentication.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
)
from addons.handlers.errors import handle_error


@extend_schema(tags=["token"])
class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=["token"])
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


@extend_schema(tags=["token"])
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer


@extend_schema(tags=["logout"])
class UserLogoutView(APIView):
    """
    For authenticated users only
    This view is for adding refresh token to a blacklist, so user cannot refresh his access token,
    Access token is still valid and user can continue using the app until access token is expired
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # getting refresh token from request and adding it to a blacklist
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return handle_error(e)  # returns full traceback only if DEBUG = True in settings.py
