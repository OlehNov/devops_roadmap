from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def send_activation_email(request: HttpRequest, user_id: int) -> None:
    user_instance = User.objects.get(id=user_id)
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
