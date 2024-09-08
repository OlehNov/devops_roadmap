from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsNotDeleted(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_deleted:
                return False
        return True


def user_authenticated(user):
    if isinstance(user, AnonymousUser):
        raise PermissionDenied("Forbidden")
