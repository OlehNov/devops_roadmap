from django.db import transaction
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from admins.serializers import AdminDeactivateSerializer, AdminSerializer
from eventlogs.mixins import EventLogMixin
from roles.constants import Role
from users.models import User
from users.permissions import IsNotDeleted, IsSuperuser


class AdminListAPIView(ListAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, IsSuperuser]
    lookup_url_kwarg = "admin_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        if user.role == Role.ADMIN or user.is_staff:
            return User.objects.filter(role=Role.ADMIN)

        return User.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class AdminRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, IsSuperuser]
    lookup_url_kwarg = "admin_id"

    def get_object(self):
        admin = get_object_or_404(
            User.objects.filter(role=1), id=self.kwargs.get("admin_id")
        )
        return admin

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        admin = self.get_object()
        deactivate_serializer = AdminDeactivateSerializer(
            admin, data={"is_deleted": True, "is_active": False}
        )

        if deactivate_serializer.is_valid():
            deactivate_serializer.save()
            return Response(
                {"detail": "User has been deleted"}, status=HTTP_204_NO_CONTENT
            )

        return Response(deactivate_serializer.errors, status=HTTP_400_BAD_REQUEST)
