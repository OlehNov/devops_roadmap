from rest_framework.permissions import BasePermission

from glamps.permissions import user_authenticated
from roles.constants import Role


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_authenticated(request.user)

        if request.user.role == Role.ADMIN or request.user.is_staff:
            return True

        if request.user.role == Role.ADMIN and obj.user == request.user:
            return True

        return False
