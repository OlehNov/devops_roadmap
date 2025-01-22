import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from addons.mixins.eventlog import EventLogMixin
from roles.constants import Role
from users.permissions import IsAuthenticatedOrForbidden
from users.serializers import (
    CurrentUserSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserSerializer
)
from users.tasks import send_reset_password_email

User = get_user_model()


@extend_schema(tags=["user"])
class UserViewSet(ModelViewSet, EventLogMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        if user.role == Role.ADMIN or user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=user.id)

    @action(detail=False, methods=["get", "GET"], url_path="current-user")
    def current_user(self, request):
        serializer = CurrentUserSerializer(self.request.user)
        return Response(serializer.data, 200)

    def perform_create(self, serializer):
        model = serializer.save()
        validated_data = serializer.validated_data
        self.log_event(
            self.request, operated_object=model, validated_data=validated_data
        )
        return model

    def perform_update(self, serializer):
        model = serializer.save()
        validated_data = serializer.validated_data
        self.log_event(
            self.request, operated_object=model, validated_data=validated_data
        )
        return model

    def perform_destroy(self, model):
        self.log_event(self.request, operated_object=model)
        return super().perform_destroy(model)

@extend_schema(tags=["password"])
class PasswordResetRequestView(APIView):
    permission_classes = [IsAuthenticatedOrForbidden]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = get_object_or_404(
                User, email=serializer.validated_data["email"]
            )
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse(
                    "users:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
            )

            send_reset_password_email.apply_async(args=[user.email, reset_url])

            return Response(
                {"detail": "Password reset email has been sent."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["password"])
class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticatedOrForbidden]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
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
                    {"detail": "Password has been reset."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
        )
