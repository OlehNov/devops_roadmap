from celery import shared_task
from django.http import HttpRequest

from users.services.emails import send_activation_email, send_reset_password


@shared_task
def verify_email(request: HttpRequest, user_id: int) -> None:
    send_activation_email(request, user_id)


@shared_task
def send_reset_password_email(email, reset_url):
    send_reset_password(email, reset_url)
