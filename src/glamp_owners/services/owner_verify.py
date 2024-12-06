import os
import random

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from dotenv import load_dotenv

from users.utils import TokenGenerator

load_dotenv()

User = get_user_model()


def send_verification_email(user_id: int) -> None:
    user_instance = User.objects.get(pk=user_id)

    message = render_to_string(
        "owner_verify.html",
        context={
            "user": user_instance,
            "domain": os.getenv("DOMAIN"),
        },
    )

    email = EmailMessage(
        subject="Action Required: Verify Your Account",
        body=message,
        to=[user_instance.email],
    )
    email.content_subtype = "html"
    email.send()
