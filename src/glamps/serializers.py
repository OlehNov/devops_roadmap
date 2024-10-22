from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from glamps.models import Glamp, Picture
from categories.models import Category
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = "pic"


class GlampSerializer(ModelSerializer):
    picture = PictureSerializer(many=True)
    category = CategorySerializer()
    owner = UserSerializer()

    class Meta:
        model = Glamp
        fields = "__all__"

    def create(self, validated_data):
        pic = validated_data.pop("picture")
        category = validated_data.pop("category")
        owner = validated_data.pop("owner")

        category_obj = Category.objects.get(id=category["id"])
        owner_obj = User.objects.get(id=owner["id"])

        glamp_obj = Glamp.objects.create(
            category=category_obj, owner=owner_obj, **validated_data
        )

        for picture_data in pic:
            Picture.objects.create(glamp=glamp_obj, **picture_data)

        return glamp_obj

    def update(self, instance, validated_data):
        pic = validated_data.pop("picture", None)
        category = validated_data.pop("category", None)
        owner = validated_data.pop("owner", None)

        if category:
            category_obj = Category.objects.get(id=category["id"])
            instance.category = category_obj

        if owner:
            owner_obj = User.objects.get(id=owner["id"])
            instance.owner = owner_obj

        if pic:
            instance.picture.clear()

            for picture_data in pic:
                Picture.objects.get_or_create(glamp=instance, **picture_data)

        instance.save()

        return instance
