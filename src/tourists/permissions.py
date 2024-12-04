from rest_framework.permissions import BasePermission
from roles.constants import Role
from glamps.permissions import user_authenticated


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.ADMIN or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsTourist(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.TOURIST

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
