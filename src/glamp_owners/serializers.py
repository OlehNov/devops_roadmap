from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (CharField, ModelSerializer, Serializer,
                                        ValidationError)
from rest_framework_simplejwt.tokens import RefreshToken

from glamp_owners.models import GlampOwner
from users.serializers import UserRegisterSerializer, UserSerializer
from users.utils import TokenGenerator

User = get_user_model()


class GlampOwnerRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = GlampOwner
        fields = ["user", "status", "first_name", "last_name", "phone"]
        read_only_fields = ["status"]


class GlampOwnerSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GlampOwner
        fields = "__all__"
        read_only_fields = ["id", "status"]
