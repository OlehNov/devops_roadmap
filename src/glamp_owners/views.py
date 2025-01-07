from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from addons.mixins.eventlog import EventLogMixin
from glamp_owners.models import GlampOwner
from glamp_owners.permissions import IsAdministrator, IsManager, IsOwner
from glamp_owners.serializers import (
    GlampOwnerRegisterSerializer,
    GlampOwnerSerializer,
)
from glamp_owners.tasks import verify_glamp_owner
from roles.constants import ProfileStatus, Role
from tourists.validators import validate_phone
from users.validators import validate_first_name_last_name

User = get_user_model()


@extend_schema(tags=["glamp_owner"])
class GlampOwnerViewSet(ModelViewSet, EventLogMixin):
    queryset = GlampOwner.objects.select_related("user")
    serializer_class = GlampOwnerSerializer
    lookup_url_kwarg = "glamp_owner_id"

    def get_serializer_class(self):
        if self.action == "create":
            return GlampOwnerRegisterSerializer
        return GlampOwnerSerializer

    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [AllowAny]
            case "list":
                permission_classes = [IsAdministrator | IsManager]
            case "retrieve":
                permission_classes = [IsOwner | IsManager | IsAdministrator]
            case "update":
                permission_classes = [IsOwner | IsManager | IsAdministrator]
            case "partial_update":
                permission_classes = [IsOwner | IsManager | IsAdministrator]
            case "delete":
                permission_classes = [IsOwner | IsManager | IsAdministrator]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):

        if not request.user.is_anonymous:

            if GlampOwner.objects.filter(user=request.user).first().exists():
                return Response(
                    {
                        "detail": "User with Glamp Owner profile can't create a new Glamp Owner."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user_data = serializer.validated_data["user"]
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            phone = serializer.validated_data["phone"]

            password = user_data.get("password")
            confirm_password = user_data.pop("confirm_password")
            if password != confirm_password:
                raise ValidationError(
                    {"password": "Password fields do not match."}
                )

            validate_first_name_last_name(first_name)
            validate_first_name_last_name(last_name)
            validate_phone(phone)

            user = User.objects.create_user(
                email=user_data.get("email"),
                password=password,
                role=Role.OWNER,
                is_active=False,
                is_staff=False,
            )

            owner = GlampOwner.objects.get(id=user.id, user=user)

            if not owner:
                return Response(
                    {"detail": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            owner.first_name = first_name
            owner.last_name = last_name
            owner.phone = phone
            owner.save()

            transaction.on_commit(verify_glamp_owner(user.id))
            validated_data = serializer.validated_data

            self.log_event(request, operated_object=user, validated_data=validated_data)
            self.log_event(request, operated_object=owner, validated_data=validated_data)

            return Response(
                GlampOwnerSerializer(owner).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied("Not Allowed")

        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone": request.data.get("phone"),
        }

        if not partial:
            missing_fields = []

            for key, value in data.items():
                if value is None:
                    missing_fields.append(key)

            if missing_fields:
                return Response(
                    {
                        "detail": f"Fields {', '.join(missing_fields)} is required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        if serializer.is_valid():
            validated_data = serializer.validated_data
            self.perform_update(serializer)
            self.log_event(request, operated_object=instance, validated_data=validated_data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied("Not Allowed")

        if instance.status == ProfileStatus.DEACTIVATED:
            return Response(
                {"detail": "Not Fopund"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.status = ProfileStatus.DEACTIVATED
        instance.save()

        self.log_event(request, operated_object=instance)

        return Response(
            {"detail": "Object deactivated successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
