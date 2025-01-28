from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied


def user_authenticated(user):
    if isinstance(user, AnonymousUser):
        raise PermissionDenied("Forbidden")
    return True