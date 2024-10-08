from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsNotDeleted(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_deleted == False
        )


class IsAuthenticatedOrForbidden(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            raise PermissionDenied("Forbidden")
        return True