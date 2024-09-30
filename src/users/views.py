from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from roles.constants import Role
from users.permissions import user_authenticated
from users.serializers import (
    UserSerializer,
    CurrentUserSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ActivateUserSerializer,
)
from users.tasks import send_reset_password_email, verify_email
from users.utils import TokenGenerator
from yaml import serialize

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.ADMIN:
            return User.objects.all()

        return User.objects.filter(id=user.id)

    @action(detail=False, methods=["get", "GET"], url_path="current-user")
    def current_user(self, request):
        serializer = CurrentUserSerializer(self.request.user)
        return Response(serializer.data, 200)


class ActivateUserAPIView(APIView):
    """User activate class"""

    permission_classes = [AllowAny]
    serializer_class = ActivateUserSerializer

    def post(self, request, *args, **kwargs):
        data = {
            "uuid64": kwargs.get("uuid64"),
            "token": kwargs.get("token"),
        }
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            result = serializer.activate()  # Activate user.

            login(
                request,
                result["current_user"],
                backend="django.contrib.auth.backends.ModelBackend",
            )

            return Response(
                {
                    "detail": "User activated successfully.",
                    "current_user": result['current_user'].pk,
                    "access": result['access'],
                    "refresh": result['refresh'],
                    "user_email": result['current_user'].email,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Unexpected error."}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        user_authenticated(request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data["email"])
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse(
                "users:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            )
        )

        send_reset_password_email.apply_async(args=[user.email, reset_url])

        return Response(
            {"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        user_authenticated(request.user)

        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        token_generator = PasswordResetTokenGenerator()

        if user and token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data, user=user)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"detail": "Password has been reset."}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
        )
