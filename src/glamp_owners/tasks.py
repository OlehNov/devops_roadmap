from celery import shared_task
from django.http import HttpRequest

from glamp_owners.services.owner_verify import send_verification_email


@shared_task
def verify_glamp_owner(request: HttpRequest, user_id: int) -> None:
    send_verification_email(request, user_id)
