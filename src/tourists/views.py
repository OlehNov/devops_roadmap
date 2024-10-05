from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from eventlogs.mixins import EventLogMixin
from handlers.errors import validate_phone_error, validate_birthday_error
from roles.constants import Role
from roles.permissions import RoleIsAdmin
from tourists.models import Tourist
from tourists.serializers import (
    TouristSerializer,
    TouristDeactivateSerializer,
    UserTouristRegistrationSerializer,
)
from tourists.validators import validate_phone, validate_birthday
from users.models import User
from users.permissions import IsNotDeleted
from users.tasks import verify_email


class TouristListAPIView(ListAPIView):
    serializer_class = TouristSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]
    lookup_url_kwarg = "tourist_id"

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserTouristRegisterView(EventLogMixin, CreateAPIView):
    """User registration class"""

    serializer_class = UserTouristRegistrationSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "tourist_id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    password=serializer.validated_data["password"],
                    role=Role.TOURIST,
                )
                user.is_active = False
                user.save()

                Tourist.objects.create(user=user)
                self.log_event(request, Tourist)
        except Exception as e:
            if settings.DEBUG:
                return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
            return Response(
                {"error": "An error occurred. Please try again later."},
                status=HTTP_400_BAD_REQUEST,
            )

        verify_email.apply_async(args=[user.pk])

        return Response(serializer.data, status=HTTP_201_CREATED)


class TouristRetrieveUpdateDestroyAPIView(EventLogMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TouristSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, RoleIsAdmin]
    lookup_url_kwarg = "tourist_id"

    def _validate_phone_number(self, phone_number=None):
        if phone_number:
            try:
                validate_phone(phone_number)
            except ValidationError as e:
                validate_phone_error(e)

    def _validate_birthday_date(self, birthday_date=None):
        if birthday_date:
            try:
                validate_birthday(birthday_date)
            except ValidationError as e:
                validate_birthday(e)

    def get_object(self):
        tourist = get_object_or_404(
            User.objects.all(), id=self.kwargs.get("tourist_id")
        )
        return tourist

    def patch(self, request, *args, **kwargs):
        phone_number = request.data.get("phone", None)
        birthday_date = request.data.get("birthday", None)

        self._validate_phone_number(phone_number)
        self._validate_birthday_date(birthday_date)

        kwargs["partial"] = True

        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        phone_number = request.data.get("phone", None)
        birthday_date = request.data.get("birthday", None)

        self._validate_phone_number(phone_number)
        self._validate_birthday_date(birthday_date)

        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            self.log_event(request, instance)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        tourist = self.get_object()
        deactivate_serializer = TouristDeactivateSerializer(
            tourist, data={"is_deleted": True, "is_active": False}
        )

        if deactivate_serializer.is_valid():
            deactivate_serializer.save()
            self.log_event(request, tourist)
            return Response(
                {"detail": "User has been deleted"}, status=HTTP_204_NO_CONTENT
            )

        return Response(deactivate_serializer.errors, status=HTTP_400_BAD_REQUEST)


class CurrentTouristProfileRetrieveUpdateDestroyAPIView(EventLogMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TouristSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]
    lookup_url_kwarg = "tourist_id"

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        birthday = request.data.get("birthday", None)

        if phone:
            try:
                validate_phone(phone)
            except ValidationError as e:
                validate_phone_error(e)

        if birthday:
            try:
                validate_birthday(birthday)
            except ValidationError as e:
                validate_birthday_error(e)

        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        tourist_data = request.data.get("tourist", {})
        phone = tourist_data.get("phone", None)
        birthday = tourist_data.get("birthday", None)

        if phone:
            try:
                validate_phone(phone)
            except ValidationError as e:
                validate_phone_error(e)

        if birthday:
            try:
                validate_birthday(birthday)
            except ValidationError as e:
                validate_birthday_error(e)

        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            self.perform_update(serializer)
            self.log_event(request, instance)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
