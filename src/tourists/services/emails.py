from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpRequest
from rest_framework import status

from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


User = get_user_model()


def send_activation_email(request: HttpRequest, user_id: int) -> Response | None:
    user_instance = User.objects.get(id=user_id)

    if not user_instance:
        return Response(
            {"detail": "Not Found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    token = RefreshToken.for_user(user_instance)
    host = request.get_host()
    protocol = "https" if request.is_secure() else "http"

    context = {
        "user": user_instance.email,
        "host": host,
        "protocol": protocol,
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
