from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from managers.models import GlampManager
from users.serializers import UserRegisterSerializer, UserSerializer


User = get_user_model()


class ManagerRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = GlampManager
        fields = ["user", "status", "first_name", "last_name"]
        read_only_fields = ["status"]


class ManagerSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GlampManager
        fields = "__all__"
        read_only_fields = ["id", "status"]
