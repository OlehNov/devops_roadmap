from celery import shared_task
from django.http import HttpRequest

from tourists.services.emails import send_activation_email

@shared_task
def verify_email(request: HttpRequest, user_id: int) -> None:
    send_activation_email(request, user_id)