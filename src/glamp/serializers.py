from rest_framework.serializers import ModelSerializer

from glamp.models import Address, Attribute, AttributeGlamp, Glamp, TypeGlamp
from tourists.serializers import TouristSerializer


class TypeGlampSerializer(ModelSerializer):
    class Meta:
        model = TypeGlamp
        fields = ["id", "name"]


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ["created", "updated"]


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ["created", "updated"]


class AttributeGlampSerializer(ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = AttributeGlamp
        exclude = ["created", "updated", "glamp"]


class GlampSerializer(ModelSerializer):
    type_glamp = TypeGlampSerializer()
    address = AddressSerializer()
    attribute = AttributeGlampSerializer(read_only=True, many=True)
    owner = TouristSerializer()

    class Meta:
        model = Glamp
        exclude = ["created", "updated"]
