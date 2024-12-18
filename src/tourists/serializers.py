from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from tourists.models import Tourist
from users.serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class TouristRegisterSerializer(ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Tourist
        fields = [
            "user",
            "status",
            "first_name",
            "last_name",
            "birthday",
            "phone",
        ]
        read_only_fields = ["status"]


class TouristSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tourist
        fields = "__all__"
        read_only_fields = ["id", "status"]
