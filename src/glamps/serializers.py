from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from glamps.models import Glamp
from users.serializers import UserSerializer


class GlampSerializer(ModelSerializer):
    category = CategorySerializer()
    owner = UserSerializer()

    class Meta:
        model = Glamp
        fields = "__all__"
