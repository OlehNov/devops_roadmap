import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from dotenv import load_dotenv

from users.utils import TokenGenerator

load_dotenv()

User = get_user_model()


def send_registration_email(user_id):
    user_instance = User.objects.get(pk=user_id)
    message = render_to_string(
        "emails/registration_email.html",
        context={
            "user": user_instance,
            "domain": os.getenv("DOMAIN"),
            "uid": urlsafe_base64_encode(force_bytes(user_id)),
            "token": TokenGenerator().make_token(user_instance),
        },
    )

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
