from rest_framework.permissions import BasePermission

from glamps.permissions import user_authenticated
from roles.constants import Role


class IsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_authenticated(request.user)
        return request.user.role == Role.ADMIN and request.user.is_staff


class IsAdministrator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_authenticated(request.user)
        return request.user.role == Role.ADMIN

    def has_object_permission(self, request, view, obj):
        if obj.user.role == Role.ADMIN:
            return obj.user == request.user

        elif obj.user.role in [Role.TOURIST, Role.OWNER, Role.MANAGER]:
            return True

        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER

    def has_object_permission(self, request, view, obj):
        if obj.user.role == Role.MANAGER:
            return obj.user == request.user

        elif obj.user.role in [Role.TOURIST, Role.OWNER]:
            return True

        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.OWNER

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsTourist(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.TOURIST

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
