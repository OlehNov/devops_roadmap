from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from addons.mixins.eventlog import EventLogMixin
from managers.models import GlampManager
from managers.permissions import IsAdministrator, IsManager
# from addons.backend_filters.filter_backend import CustomBaseFilterBackend
from managers.serializers import ManagerRegisterSerializer, ManagerSerializer
from roles.constants import ProfileStatus, Role
from users.validators import validate_first_name_last_name

User = get_user_model()


@extend_schema(tags=["manager"])
class ManagerModelViewSet(ModelViewSet, EventLogMixin):
    queryset = GlampManager.objects.select_related("user")
    serializer_class = ManagerSerializer
    lookup_url_kwarg = "manager_id"
    permission_classes = [IsAdministrator | IsManager]
    # filter_backends = [CustomBaseFilterBackend]

    def get_serializer_class(self):
        if self.action == "create":
            return ManagerRegisterSerializer
        return ManagerSerializer

    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [IsAdministrator]
            case _:
                permission_classes = [IsAdministrator | IsManager]

        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user_data = serializer.validated_data["user"]
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]

            password = user_data.get("password")
            confirm_password = user_data.pop("confirm_password")

            if password != confirm_password:
                raise ValidationError(
                    {"password": "Password fields do not match."}
                )

            validate_first_name_last_name(first_name)
            validate_first_name_last_name(last_name)

            user = User.objects.create_user(
                email=user_data.get("email"),
                password=password,
                role=Role.MANAGER,
                is_active=True,
                is_staff=False,
            )

            manager = GlampManager.objects.get(id=user.id, user=user)

            manager.first_name = first_name
            manager.last_name = last_name
            manager.save()
            validated_data = serializer.validated_data

            self.log_event(request, user, validated_data=validated_data)
            self.log_event(request, manager, validated_data=validated_data)

            return Response(
                ManagerSerializer(manager).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }

        if not partial and (not data["first_name"] or not data["last_name"]):
            return Response(
                {"detail": "Both 'first_name' and 'last_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        if serializer.is_valid():
            validated_data = serializer.validated_data
            self.perform_update(serializer)
            self.log_event(request, instance, validated_data=validated_data)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == ProfileStatus.DEACTIVATED:
            return Response(
                {"detail": "Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        else:
            instance.status = ProfileStatus.DEACTIVATED
            instance.save()

            self.log_event(request, instance)

            return Response(
                {"detail": "Object deactivated successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
