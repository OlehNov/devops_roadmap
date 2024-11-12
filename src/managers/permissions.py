import logging
from rest_framework.permissions import BasePermission
from roles.constants import Role
from glamps.permissions import user_authenticated

logger = logging.getLogger(__name__)


class IsAdminOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_authenticated(request.user)

        if request.user.role == Role.ADMIN or request.user.is_staff:
            return True

        if request.user.role == Role.MANAGER and obj.user == request.user:
            return True

        return False
