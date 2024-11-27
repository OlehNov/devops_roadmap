from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from administrators.models import Administrator
from users.serializers import UserRegisterSerializer, UserSerializer


User = get_user_model()


class AdministratorRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Administrator
        fields = ["user", "status", "first_name", "last_name"]
        read_only_fields = ["id", "status"]


class AdministratorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = "__all__"
        read_only_fields = ["id", "status"]
