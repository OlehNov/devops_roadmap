import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from addons.mixins.eventlog import EventLogMixin
from addons.permissions.permissions import (
    IsAdministrator,
    IsManager,
    IsObjOwner,
    IsStaffAdministrator
)
from glamp_owners.models import GlampOwner
from glamp_owners.serializers import (
    GlampOwnerRegisterSerializer,
    GlampOwnerSerializer
)
from glamp_owners.tasks import verify_glamp_owner
from roles.constants import ProfileStatus
from tourists.validators import validate_phone
from users.validators import validate_first_name_last_name


User = get_user_model()


@extend_schema(tags=["glamp_owner"])
class GlampOwnerViewSet(ModelViewSet, EventLogMixin):
    queryset = GlampOwner.objects.select_related("user")
    serializer_class = GlampOwnerSerializer
    lookup_url_kwarg = "glamp_owner_id"
    http_method_names = ["get", "put", "patch", "delete"]

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [IsManager | IsAdministrator | IsStaffAdministrator]
            case "retrieve":
                permission_classes = [IsObjOwner | IsManager | IsAdministrator | IsStaffAdministrator]
            case "update":
                permission_classes = [IsObjOwner | IsManager | IsAdministrator | IsStaffAdministrator]
            case "partial_update":
                permission_classes = [IsObjOwner | IsManager | IsAdministrator | IsStaffAdministrator]
            case "destroy":
                permission_classes = [IsManager | IsAdministrator | IsStaffAdministrator]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

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

        if instance.status == ProfileStatus.DEACTIVATED:
            return Response(
                {"detail": "Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.status = ProfileStatus.DEACTIVATED
        instance.save()

        self.log_event(request, operated_object=instance)

        return Response(
            {"detail": "Object deactivated successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

@extend_schema(tags=["register-glamp_owner"])
class GlampOwnerRegisterView(APIView, EventLogMixin):
    serializer_class = GlampOwnerRegisterSerializer
    permission_classes = [AllowAny]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = GlampOwnerRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            created_user = serializer.save()

            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            phone = serializer.validated_data["phone"]

            validate_first_name_last_name(first_name)
            validate_first_name_last_name(last_name)
            validate_phone(phone)

            owner = GlampOwner.objects.get(id=created_user.id)

            if not owner:
                return Response(
                    {"detail": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            owner.first_name = first_name
            owner.last_name = last_name
            owner.phone = phone
            owner.save()

            transaction.on_commit(lambda: verify_glamp_owner(request, created_user.id))

            validated_data = serializer.validated_data

            self.log_event(request, operated_object=created_user, validated_data=validated_data)
            self.log_event(request, operated_object=owner, validated_data=validated_data)

            return Response(
                GlampOwnerSerializer(owner).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["activate-glamp_owner"])
class ActivateGlampOwnerView(APIView, EventLogMixin):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")

        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, settings.ALGORITHM
            )

            owner = get_object_or_404(GlampOwner, id=decoded_token["user_id"])

            owner.is_verified = True
            owner.user.is_active = True

            owner.user.save()
            owner.save()

            login(request, owner.user)

            refresh_token = RefreshToken.for_user(owner.user)

            return Response(
                {
                    "detail": "Owner has been activated.",
                    "email": owner.user.email,
                    "user_id": owner.user.id,
                    "token": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "Activation link has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.InvalidTokenError:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

