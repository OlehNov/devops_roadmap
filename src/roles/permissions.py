from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from roles.constants import Role

User = get_user_model()


def user_authenticated(user):
    if isinstance(user, AnonymousUser):
        raise PermissionDenied("Forbidden")


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER


class RoleIsTourist(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.TOURIST


class RoleIsOwner(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.OWNER


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.role == Role.ADMIN
