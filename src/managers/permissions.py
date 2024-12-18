from rest_framework.permissions import BasePermission

from glamps.permissions import user_authenticated
from roles.constants import Role


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.ADMIN

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
