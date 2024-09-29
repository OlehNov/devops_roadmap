from rest_framework.serializers import ModelSerializer

from glamps.models import Glamp
from users.serializers import UserSerializer


class GlampSerializer(ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Glamp
        fields = '__all__'
