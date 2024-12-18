from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()


def email_sender(subject: str, message: str, recipient: str) -> None:
    email = EmailMessage(
        subject=subject,
        body=message,
        to=[recipient],
    )

    email.content_subtype = 'text/html'
    email.send()
