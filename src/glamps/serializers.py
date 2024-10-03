from rest_framework.serializers import ModelSerializer

from glamps.models import Glamp
from users.serializers import UserSerializer
from categories.serializers import CategorySerializer


class GlampSerializer(ModelSerializer):
    category = CategorySerializer()
    owner = UserSerializer()

    class Meta:
        model = Glamp
        fields = '__all__'
