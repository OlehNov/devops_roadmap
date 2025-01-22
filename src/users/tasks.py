from celery import shared_task

from users.services.emails import send_activation_email, send_reset_password


@shared_task
def send_reset_password_email(email, reset_url):
    send_reset_password(email, reset_url)
