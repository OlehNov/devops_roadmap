from rest_framework.serializers import ModelSerializer

from categories.serializers import CategorySerializer
from rest_framework import serializers
from glamps.models import Glamp, Picture
from categories.models import Category
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = ["pic"]


class GlampSerializer(ModelSerializer):
    # picture = PictureSerializer(many=True)
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Glamp
        fields = "__all__"

    def create(self, validated_data):
        #pic = validated_data.pop("picture")

        glamp_obj = Glamp.objects.create(
            owner=self.context["request"].user, **validated_data
        )

        # for picture_data in pic:
        #     Picture.objects.create(glamp=glamp_obj, **picture_data)

        return glamp_obj

    def update(self, instance, validated_data):
        # pic = validated_data.pop("picture", None)
        category = validated_data.pop("category", None)

        if category:
            if isinstance(category, Category):
                instance.category = category
            else:
                instance.category = Category.objects.get(id=category)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # if pic:
        #     instance.picture.clear()
        #
        #     for picture_data in pic:
        #         Picture.objects.get_or_create(glamp=instance, **picture_data)

        instance.save()

        return instance
