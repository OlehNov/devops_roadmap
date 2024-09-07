from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config import settings
from tourists.serializers import UserTouristProfileSerializer
from rest_framework.exceptions import PermissionDenied
from tourists.validators import validate_phone, validate_birthday
from users.models import User
from roles.constants import Role
from handlers.errors import validate_phone_error, validate_birthday_error

import traceback


class TouristProfileListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TouristProfileDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_object(self):
        user = self.request.user
        queryset = self.get_queryset()

        if user.role == Role.ADMIN:
            target_user = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        else:
            if settings.DEBUG:
                raise PermissionDenied(
                    detail={
                        "detail": "You don't have enough permission.",
                        "traceback": traceback.format_exc()
                    }
                )
            else:
                raise PermissionDenied({"detail": "You don't have enough permission."})

        return target_user

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        tourist_data = request.data.get('tourist', {})
        phone = tourist_data.get('phone', None)
        birthday = tourist_data.get('birthday', None)

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

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        target_user = self.get_object()

        target_user.is_active = False
        target_user.save()

        return Response({"detail": "User has been deactivated."}, status=status.HTTP_204_NO_CONTENT)


class CurrentUserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        tourist_data = request.data.get('tourist', {})
        phone = tourist_data.get('phone')
        birthday = tourist_data.get('birthday')

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

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
