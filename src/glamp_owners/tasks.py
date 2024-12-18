from celery import shared_task

from glamp_owners.services.owner_verify import send_verification_email


@shared_task
def verify_glamp_owner(user_id: int):
    send_verification_email(user_id)
