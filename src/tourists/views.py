from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config import settings
from tourists.serializers import UserTouristProfileSerializer
from tourists.validators import validate_phone, validate_birthday
from users.models import User
from roles.constants import Role


class TouristProfileView(generics.ListCreateAPIView):
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


class TouristProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
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
            obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        else:
            raise PermissionDenied("You do not have permission to update this profile.()")

        return obj

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user = self.request.user

        if user.role != Role.ADMIN:
            raise PermissionDenied("You do not have permission to update this profile.()(")

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
                if settings.DEBUG:
                    return Response({"phone": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'phone': "Validation error. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."},
                                    status=status.HTTP_400_BAD_REQUEST)

        if birthday:
            try:
                validate_birthday(birthday)
            except ValidationError as e:
                if settings.DEBUG:
                    return Response({"birthday": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'birthday': "Validation error. The date should be specified in the format YYYY-MM-DD"},
                                    status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response(serializer.data)


class CurrentUserProfileView(generics.RetrieveUpdateDestroyAPIView):
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
                return Response(
                    {"phone": str(e) if settings.DEBUG else "Validation error. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if birthday:
            try:
                validate_birthday(birthday)
            except ValidationError as e:
                return Response(
                    {"birthday": str(e) if settings.DEBUG else "Validation error. The date should be specified in the format YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        self.perform_update(serializer)
        return Response(serializer.data)