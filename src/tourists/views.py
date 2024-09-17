from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tourists.serializers import UserTouristProfileSerializer, TouristDeactivateSerializer
from tourists.validators import validate_phone, validate_birthday
from users.models import User
from users.permissions import IsNotDeleted
from roles.constants import Role
from roles.permissions import RoleIsAdmin, RoleIsManager, IsOwner, RoleIsTourist
from handlers.errors import validate_phone_error, validate_birthday_error


class TouristProfileListCreateAPIView(ListCreateAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_200_OK, headers=headers)


class TouristProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted, RoleIsAdmin]

    def get_object(self):
        tourist = get_object_or_404(User.objects.all(), pk=self.kwargs.get('pk'))
        return tourist

    def patch(self, request, *args, **kwargs):
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

        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
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

        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            self.perform_update(serializer)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        tourist = self.get_object()
        deactivate_serializer = TouristDeactivateSerializer(tourist, data={'is_deleted': True, 'is_active': False}, partial=True)

        if deactivate_serializer.is_valid():
            deactivate_serializer.save()
            return Response({"detail": "User has been deactivated."}, status=HTTP_204_NO_CONTENT)
        else:
            return Response(deactivate_serializer.errors, status=HTTP_400_BAD_REQUEST)



class CurrentUserProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserTouristProfileSerializer
    permission_classes = [IsAuthenticated, IsNotDeleted]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
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

        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
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

        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            self.perform_update(serializer)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

