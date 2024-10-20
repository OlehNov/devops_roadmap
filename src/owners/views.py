from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsNotDeleted, IsSuperuser
from django.db import transaction
from roles.constants import Role
from tourists.validators import validate_phone
from django.core.exceptions import ValidationError
from handlers.errors import validate_phone_error
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from owners.models import Owner
from owners.serializers import (
    OwnerRegistrationSerializer,
    OwnerSerializer,
    OwnerDeactivateSerializer,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from roles.permissions import (
    IsAdminOrSuperuser
)
from users.tasks import verify_email


User = get_user_model()

class OwnerRegisterView(CreateAPIView):
    """Owner registration class"""

    serializer_class = OwnerRegistrationSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "owner_id"

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

                    Owner.objects.create(user=user)

            except Exception as e:
                if settings.DEBUG:
                    return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
                return Response(
                    {"error": "An error occurred. Please try again later."},
                    status=HTTP_400_BAD_REQUEST,
                )

            verify_email.apply_async(args=[user.pk])

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OwnerListAPIView(ListAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]
    lookup_url_kwarg = "owner_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return User.objects.none()

        if user.role == Role.ADMIN or user.is_staff:
            return User.objects.filter(role=Role.OWNER)

        if user.role == Role.OWNER:
            return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class OwnerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, IsAdminOrSuperuser]
    lookup_url_kwarg = "owner_id"

    def _validate_phone_number(self, phone_number=None):
        if phone_number:
            try:
                validate_phone(phone_number)
            except ValidationError as e:
                validate_phone_error(e)

    def get_object(self):
        owner = get_object_or_404(
            User.objects.all(), id=self.kwargs.get("owner_id")
        )
        return owner

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
        owner = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(owner, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        owner = self.get_object()
        deactivate_serializer = OwnerDeactivateSerializer(
            owner, data={"is_deleted": True, "is_active": False}
        )

        if deactivate_serializer.is_valid():
            deactivate_serializer.save()
            return Response(
                {"detail": "Owner has been deleted"}, status=HTTP_204_NO_CONTENT
            )

        return Response(deactivate_serializer.errors, status=HTTP_400_BAD_REQUEST)
