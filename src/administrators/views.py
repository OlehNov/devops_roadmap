from rest_framework.viewsets import ModelViewSet
from administrators.models import Administrator
from addons.backend_filters.filter_backend import CustomBaseFilterBackend
from administrators.serializers import (
    AdministratorSerializer,
    AdministratorRegisterSerializer,
)
from administrators.permissions import IsAdmin
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from roles.constants import ProfileStatus
from rest_framework import status


@extend_schema(tags=["administrator"])
class AdministratorModelViewSet(ModelViewSet):
    queryset = Administrator.objects.select_related("user")
    serializer_class = AdministratorSerializer
    permission_classes = [IsAdmin]
    filter_backends = [CustomBaseFilterBackend]

    def get_serializer_class(self):
        if self.action == "create":
            return AdministratorRegisterSerializer
        return AdministratorSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = ProfileStatus.DEACTIVATED

        instance.save()

        return Response(
            {"detail": "Object deactivated successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
