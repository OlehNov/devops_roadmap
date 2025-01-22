from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model, login
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from addons.mixins.eventlog import EventLogMixin
from roles.constants import ProfileStatus
from tourists.models import Tourist
from addons.permissions.permissions import (
    IsAdministrator,
    IsManager,
    IsTourist,
    IsStaffAdministrator,
)
from tourists.serializers import TouristRegisterSerializer, TouristSerializer
from tourists.validators import validate_birthday, validate_phone
from tourists.tasks import verify_email
from users.validators import validate_first_name_last_name


User = get_user_model()


@extend_schema(tags=["tourist"])
class TouristViewSet(ModelViewSet, EventLogMixin):
    queryset = Tourist.objects.select_related("user")
    serializer_class = TouristSerializer
    lookup_url_kwarg = "tourist_id"
    http_method_names = ["get", "put", "patch", "delete"]

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [
                    IsAdministrator | IsManager | IsStaffAdministrator
                ]
            case "retrieve":
                permission_classes = [
                    IsTourist
                    | IsManager
                    | IsAdministrator
                    | IsStaffAdministrator
                ]
            case "update":
                permission_classes = [
                    IsTourist
                    | IsManager
                    | IsAdministrator
                    | IsStaffAdministrator
                ]
            case "partial_update":
                permission_classes = [
                    IsTourist
                    | IsManager
                    | IsAdministrator
                    | IsStaffAdministrator
                ]
            case "delete":
                permission_classes = [
                    IsTourist
                    | IsManager
                    | IsAdministrator
                    | IsStaffAdministrator
                ]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied("Not Allowed")

        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "birthday": request.data.get("birthday"),
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
            self.log_event(
                request,
                operated_object=instance,
                validated_data=validated_data,
            )

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
                {"detail": "Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        else:
            instance.status = ProfileStatus.DEACTIVATED
            instance.save()

            self.log_event(request, operated_object=instance)

            return Response(
                {"detail": "Object deactivated successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

@extend_schema(tags=["register-tourist"])
class TouristRegisterView(APIView, EventLogMixin):
    serializer_class = TouristRegisterSerializer
    permission_classes = [AllowAny]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = TouristRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            created_user = serializer.save()

            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            birthday = serializer.validated_data["birthday"]
            phone = serializer.validated_data["phone"]

            validate_first_name_last_name(first_name)
            validate_first_name_last_name(last_name)
            validate_birthday(birthday)
            validate_phone(phone)

            tourist = Tourist.objects.get(id=created_user.id)

            if not tourist:
                return Response(
                    {"detail": "Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            tourist.first_name = first_name
            tourist.last_name = last_name
            tourist.birthday = birthday
            tourist.phone = phone
            tourist.save()

            transaction.on_commit(lambda: verify_email(request, created_user.id))

            validated_data = serializer.validated_data

            self.log_event(
                request, operated_object=created_user, validated_data=validated_data
            )
            self.log_event(
                request, operated_object=tourist, validated_data=validated_data
            )

            return Response(
                TouristSerializer(tourist).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["activate-tourist"])
class ActivateTouristView(APIView):
    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")

        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, settings.ALGORITHM
            )

            tourist = get_object_or_404(Tourist, id=decoded_token["user_id"])
            tourist.user.is_active = True
            tourist.user.save()

            login(request, tourist.user)

            refresh_token = RefreshToken.for_user(tourist.user)

            return Response(
                {
                    "detail": "Tourist has been activated.",
                    "email": tourist.user.email,
                    "user_id": tourist.user.id,
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
