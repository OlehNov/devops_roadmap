from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from addons.handlers.auth_handler import user_authenticated
from roles.constants import Role


class IsAnonymousUser(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, AnonymousUser)


class IsStaffAdministrator(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(request.user)
        return request.user.role == Role.ADMIN and request.user.is_staff


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(request.user)
        return request.user.role == Role.ADMIN


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.OWNER


class IsTourist(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.TOURIST


class IsObjOwner(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
