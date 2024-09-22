from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from roles.constants import Role
from tourists.models import Tourist
from users.permissions import user_authenticated
from users.serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserTouristRegistrationSerializer
)
from users.tasks import send_reset_password_email, verify_email
from users.utils import TokenGenerator

User = get_user_model()


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        login(request, user)
        subject = "Welcome to GLAMP"
        message = f"HI {user.username}, thank you for registering in GLAMP."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            user.email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect("/dashboard/")
    return render(request, 'mail_notification.html')


class UserTouristRegisterView(generics.CreateAPIView):
    """User registration class"""

    serializer_class = UserTouristRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    password=serializer.validated_data['password'],
                    role=Role.TOURIST
                )
                user.is_active = False
                user.save()

                Tourist.objects.create(user=user)

        except Exception as e:
            if settings.DEBUG:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "An error occurred. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)

        verify_email.apply_async(args=[user.pk])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateUserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        uuid64 = kwargs.get('uuid64')
        token = kwargs.get('token')
        pk = force_str(urlsafe_base64_decode(uuid64))
        current_user = get_object_or_404(User, pk=pk)
        user_email = current_user.email

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            refresh = RefreshToken.for_user(current_user)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')

            return Response({
                "detail": "User activated successfully.",
                "user": pk,
                "access": new_access_token,
                "refresh": new_refresh_token,
                "user_email": user_email
            }, status=status.HTTP_200_OK)

        return Response({"error": "Unexpected error."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        user_authenticated(request.user)

        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data['email'])
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        send_reset_password_email.apply_async(args=[user.email, reset_url])

        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        user_authenticated(request.user)

        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        token_generator = PasswordResetTokenGenerator()

        if user and token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data, user=user)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

