import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.urls import reverse


load_dotenv()

User = get_user_model()


def send_registration_email(user_id: int) -> None:
    user_instance = User.objects.get(pk=user_id)
    domain = os.getenv("DOMAIN")
    token = RefreshToken.for_user(user_instance)

    context = {
        "user": user_instance,
        "domain": domain,
        "token": str(token),
    }

    message = render_to_string("emails/activation_email.html", context)

    email = EmailMessage(
        subject="Activate your account",
        body=message,
        to=[user_instance.email],
    )
    email.content_subtype = "html"
    email.send()


def send_reset_password(email, reset_url):
    subject = "Password Reset Requested"
    message = f"Click the link below to reset your password:\n\n{reset_url}"
    from_email = os.getenv(
        settings.EMAIL_HOST_USER, default=settings.DEFAULT_FROM_EMAIL
    )
    send_mail(subject, message, from_email, [email])
