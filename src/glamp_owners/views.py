from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated

from addons.mixins.eventlog import EventLogMixin
# from addons.backend_filters.filter_backend import CustomBaseFilterBackend
from users.permissions import IsNotDeleted
from django.db import transaction
from roles.constants import Role
from tourists.validators import validate_phone
from django.core.exceptions import ValidationError
from addons.handlers.errors import validate_phone_error, handle_error
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from glamp_owners.models import GlampOwner
from glamp_owners.serializers import (
    GlampOwnerRegistrationSerializer,
    GlampOwnerSerializer,
    GlampOwnerDeactivateSerializer,
)
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from roles.permissions import IsAdminOrSuperuser
from users.tasks import verify_email


User = get_user_model()


@extend_schema(
    tags=["glamp-owner"],
)
class GlampOwnerRegisterView(CreateAPIView, EventLogMixin):
    """GlampOwner registration class"""

    serializer_class = GlampOwnerRegistrationSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "glampowner_id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        email=serializer.validated_data["email"],
                        first_name=serializer.validated_data["first_name"],
                        last_name=serializer.validated_data["last_name"],
                        password=serializer.validated_data["password"],
                        role=Role.OWNER,
                    )
                    user.is_active = False
                    user.save()

                    glamp_owner = GlampOwner.objects.create(user=user)
                    self.log_event(request=request, operated_object=user)
                    self.log_event(request=request, operated_object=glamp_owner)

            except Exception as e:
                handle_error(e)

            verify_email.apply_async(args=[user.pk])

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["glamp-owner"],
)
class GlampOwnerListAPIView(ListAPIView):
    serializer_class = GlampOwnerSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]
    # filter_backends = [CustomBaseFilterBackend]
    lookup_url_kwarg = "glampowner_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        if user.role == Role.ADMIN or user.is_staff or user.is_superuser:
            return User.objects.filter(role=Role.OWNER)

        if user.role == Role.OWNER:
            return User.objects.filter(id=user.id)

        return User.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"detail": "Not found"}, status=HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(
    tags=["glamp-owner"],
)
class GlampOwnerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, EventLogMixin):
    serializer_class = GlampOwnerSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, IsAdminOrSuperuser]
    # filter_backends = [CustomBaseFilterBackend]
    lookup_url_kwarg = "glampowner_id"

    def _validate_phone_number(self, phone_number=None):
        if phone_number:
            try:
                validate_phone(phone_number)
            except ValidationError as e:
                validate_phone_error(e)

    def get_object(self):
        glamp_owner = get_object_or_404(
            User.objects.all(), id=self.kwargs.get("glampowner_id")
        )
        return glamp_owner

    def patch(self, request, *args, **kwargs):
        phone_number = request.data.get("phone", None)

        self._validate_phone_number(phone_number)

        kwargs["partial"] = True

        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        phone_number = request.data.get("phone", None)

        self._validate_phone_number(phone_number)

        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        glamp_owner = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(glamp_owner, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            self.log_event(request, glamp_owner)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        glamp_owner = self.get_object()
        deactivate_serializer = GlampOwnerDeactivateSerializer(
            glamp_owner, data={"is_deleted": True, "is_active": False}
        )

        if deactivate_serializer.is_valid():
            deactivate_serializer.save()
            self.log_event(request, glamp_owner)
            return Response(
                {"detail": "GlampOwner has been deleted"}, status=HTTP_204_NO_CONTENT
            )

        return Response(deactivate_serializer.errors, status=HTTP_400_BAD_REQUEST)
