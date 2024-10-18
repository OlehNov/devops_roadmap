from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from glamps.models import Glamp, Picture
from users.serializers import UserSerializer


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"


class GlampSerializer(ModelSerializer):
    picture = PictureSerializer(many=True)
    category = CategorySerializer()
    owner = UserSerializer()

    class Meta:
        model = Glamp
        fields = "__all__"
