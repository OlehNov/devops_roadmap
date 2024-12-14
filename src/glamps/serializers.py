from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from slugify import slugify
from unidecode import unidecode

from categories.models import Category
from categories.serializers import CategorySerializer
from glamps.models import Glamp, Picture
from glamps.validators import validate_slug_glamp
from users.serializers import UserSerializer


User = get_user_model()


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = ["pic"]


class GlampSerializer(ModelSerializer):
    # picture = PictureSerializer(many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source='category', required=True
    )
    owner = UserSerializer(read_only=True)
    glamp_type = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=225)
    capacity = serializers.IntegerField(required=True, min_value=1)
    status = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, max_length=5000)
    street = serializers.CharField(required=True, max_length=225)
    number_of_bedrooms = serializers.IntegerField(required=True)
    number_of_beds = serializers.IntegerField(required=True)
    number_of_bathrooms = serializers.IntegerField(required=True)

    class Meta:
        model = Glamp
        fields = "__all__"

    def validate(self, attrs):
        transliterated_name = unidecode(attrs["name"])
        slug = slugify(transliterated_name)
        validate_slug_glamp(slug)  # Check that the slug has more than 0 characters.
        attrs["slug"] = slug

        return attrs

    def create(self, validated_data):
        #pic = validated_data.pop("picture")

        glamp_obj = Glamp.objects.create(
            owner=self.context["request"].user, **validated_data
        )
        glamp_obj.slug = f"{glamp_obj.id}-{slugify(unidecode(glamp_obj.name))}"
        glamp_obj.save()

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

        glamp = super().update(instance, validated_data)
        if "name" in validated_data:
            glamp.slug = f"{glamp.id}-{slugify(unidecode(validated_data['name']))}"
            glamp.save()

        return instance


class GlampByCategoryViewSet(ModelSerializer):
    # picture = PictureSerializer(many=True)
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    glamp_type = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=225)
    capacity = serializers.IntegerField(required=True, min_value=1)
    status = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, max_length=5000)
    street = serializers.CharField(required=True, max_length=225)
    number_of_bedrooms = serializers.IntegerField(required=True)
    number_of_beds = serializers.IntegerField(required=True)
    number_of_bathrooms = serializers.IntegerField(required=True)

    class Meta:
        model = Glamp
        fields = "__all__"

    def validate(self, attrs):
        transliterated_name = unidecode(attrs["name"])
        slug = slugify(transliterated_name)
        validate_slug_glamp(slug)  # Check that the slug has more than 0 characters.
        attrs["slug"] = slug

        return attrs

    def create(self, validated_data):
        # pic = validated_data.pop("picture")

        glamp_obj = Glamp.objects.create(
            owner=self.context["request"].user, **validated_data
        )
        glamp_obj.slug = f"{glamp_obj.id}-{slugify(unidecode(glamp_obj.name))}"
        glamp_obj.save()

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

        glamp = super().update(instance, validated_data)
        if "name" in validated_data:
            glamp.slug = f"{glamp.id}-{slugify(unidecode(validated_data['name']))}"
            glamp.save()

        return instance