from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from roles.constants import ProfileStatus, Role

from addons.mixins.eventlog import EventLogMixin
from tourists.models import Tourist
from tourists.serializers import TouristSerializer, TouristRegisterSerializer
from rest_framework.permissions import AllowAny
from users.validators import validate_first_name_last_name
from tourists.validators import validate_birthday, validate_phone
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from users.tasks import verify_email
from addons.handlers.errors import handle_error
from rest_framework.response import Response
from tourists.permissions import IsAdministrator, IsTourist, IsManager


User = get_user_model()


@extend_schema(tags=["tourist"])
class TouristViewSet(ModelViewSet, EventLogMixin):
    queryset = Tourist.objects.select_related("user")
    serializer_class = TouristSerializer
    lookup_url_kwarg = "tourist_id"

    def get_serializer_class(self):
        if self.action == "create":
            return TouristRegisterSerializer
        return TouristSerializer

    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [AllowAny]
            case "list":
                permission_classes = [IsAdministrator | IsManager]
            case "retrieve":
                permission_classes = [IsTourist | IsManager | IsAdministrator]
            case "update":
                permission_classes = [IsTourist | IsManager | IsAdministrator]
            case "partial_update":
                permission_classes = [IsTourist | IsManager | IsAdministrator]
            case "delete":
                permission_classes = [IsTourist | IsManager | IsAdministrator]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user_data = serializer.validated_data["user"]
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            birthday = serializer.validated_data["birthday"]
            phone = serializer.validated_data["phone"]

            password = user_data.get("password")
            confirm_password = user_data.pop("confirm_password")
            if password != confirm_password:
                raise ValidationError(
                    {"password": "Password fields do not match."}
                )

            validate_first_name_last_name(first_name)
            validate_first_name_last_name(last_name)
            validate_birthday(birthday)
            validate_phone(phone)

            user = User.objects.create_user(
                email=user_data.get("email"),
                password=password,
                role=Role.TOURIST,
                is_active=False,
                is_staff=False,
            )

            try:
                tourist = Tourist.objects.get(id=user.id, user=user)

                tourist.first_name = first_name
                tourist.last_name = last_name
                tourist.birthday = birthday
                tourist.phone = phone
                tourist.save()

                transaction.on_commit(verify_email(user.id))

            except Exception as e:
                handle_error(e)

            self.log_event(request, operated_object=user)
            self.log_event(request, operated_object=tourist)

            return Response(
                TouristSerializer(tourist).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

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
            self.perform_update(serializer)
            self.log_event(request, operated_object=instance)

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

        else:
            instance.status = ProfileStatus.DEACTIVATED
            instance.save()

            self.log_event(request, operated_object=instance)

            return Response(
                {"detail": "Object deactivated successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
