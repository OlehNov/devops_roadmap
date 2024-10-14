from django.db import transaction
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from eventlogs.mixins import EventLogMixin
from admins.serializers import AdminSerializer, AdminDeactivateSerializer
from users.models import User
from rest_framework.response import Response
from users.permissions import IsSuperuser, IsNotDeleted
from rest_framework.permissions import IsAuthenticated


class AdminListAPIView(ListAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, IsSuperuser]
    lookup_url_kwarg = "admin_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        return User.objects.filter(role=1)

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
