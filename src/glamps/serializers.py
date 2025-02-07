import os

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from slugify import slugify
from unidecode import unidecode

from categories.models import Category
from categories.serializers import CategorySerializer
from config import settings
from glamps.models import Glamp
from glamps.models.glamp import ImageList
from glamps.validators import (
    validate_glamp_price,
    validate_premium_level,
    validate_slug_glamp,
    validate_status,
    validate_type
)
from roles.constants import Role
from users.serializers import UserSerializer
from addons.upload_images.downloaders import upload_to, process_image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageList
        fields = ["id", "images_list"]


class GlampSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source="category",
        required=True,
    )
    owner = UserSerializer(read_only=True)
    glamp_type = serializers.IntegerField(
        required=True, validators=[validate_type]
    )
    name = serializers.CharField(required=True, max_length=225)
    capacity = serializers.IntegerField(required=True, min_value=1)
    status = serializers.IntegerField(
        required=True, validators=[validate_status]
    )
    description = serializers.CharField(required=True, max_length=5000)
    street = serializers.CharField(required=True, max_length=225)
    number_of_bedrooms = serializers.IntegerField(required=True)
    number_of_beds = serializers.IntegerField(required=True)
    number_of_bathrooms = serializers.IntegerField(required=True)
    price = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[validate_glamp_price],
    )
    is_active = serializers.BooleanField(required=False, read_only=True)
    is_hidden = serializers.BooleanField(required=False, read_only=True)
    is_verified = serializers.BooleanField(required=False, read_only=True)
    is_approved = serializers.BooleanField(required=False, read_only=True)
    rating = serializers.FloatField(required=False, read_only=True)
    premium_level = serializers.IntegerField(required=False, read_only=True)
    priority = serializers.FloatField(required=False, read_only=True)
    thumb = serializers.SerializerMethodField()
    images_list = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    thumb_list = serializers.SerializerMethodField()


    class Meta:
        model = Glamp
        fields = "__all__"

    def validate(self, attrs):
        transliterated_name = unidecode(attrs["name"])
        slug = slugify(transliterated_name)
        validate_slug_glamp(
            slug
        )  # Check that the slug has more than 0 characters.
        attrs["slug"] = slug

        return attrs

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        compressed_image = process_image(image)

        uploaded_images = validated_data.pop("uploaded_images", [])

        glamp_obj = Glamp.objects.create(
            owner=self.context["request"].user,
            image=compressed_image,
            **validated_data
        )
        glamp_obj.slug = f"{glamp_obj.id}-{slugify(unidecode(glamp_obj.name))}"

        for image in uploaded_images:
            compressed_image = process_image(image)
            image_list_obj = ImageList.objects.create(images_list=compressed_image, parent=glamp_obj)
            image_list_obj.thumbs_list = image_list_obj.thumbs_list.url
            image_list_obj.save()

        glamp_obj.thumb = glamp_obj.thumb.url
        glamp_obj.save()

        return glamp_obj

    def update(self, instance, validated_data):
        category = validated_data.pop("category", None)

        if category:
            if isinstance(category, Category):
                instance.category = category
            else:
                instance.category = Category.objects.get(id=category)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        glamp = super().update(instance, validated_data)
        if "name" in validated_data:
            glamp.slug = (
                f"{glamp.id}-{slugify(unidecode(validated_data['name']))}"
            )
            glamp.save()

        return instance

    def get_thumb(self, obj):
        if obj.image:
            from urllib.parse import urljoin

            original_path = os.path.basename(obj.thumb.name)
            thumb_name = upload_to(obj, original_path)
            print(thumb_name)
            print(original_path)

            base_path = thumb_name.split("/")[1:-1]
            thumb_path = settings.IMAGE_ROOT + "/".join(base_path) + settings.THUMB_ROOT + original_path.split("/")[-1]

            print(base_path)
            print(thumb_path)
            return self.context["request"].build_absolute_uri(
                urljoin(settings.MEDIA_URL, thumb_path)
            )

        return None

    def get_thumb_list(self, obj):
        from urllib.parse import urljoin

        thumbs = []
        for image_obj in obj.images_list.all():
            if image_obj.thumbs_list:
                original_path = os.path.basename(image_obj.thumbs_list.name)
                thumb_name = upload_to(image_obj, original_path)

                base_path = thumb_name.split("/")[1:-1]
                thumb_path = settings.IMAGE_ROOT + "/".join(base_path) + settings.THUMB_ROOT + original_path.split("/")[-1]

                thumbs.append(self.context["request"].build_absolute_uri(
                    urljoin(settings.MEDIA_URL, thumb_path)
                ))

        return thumbs if thumbs else None

    def get_images_list(self, obj):
        request = self.context.get("request")
        image_urls = [
            request.build_absolute_uri(image_obj.images_list.url)
            for image_obj in obj.images_list.all()
            if image_obj.images_list
        ]
        return image_urls if image_urls else None

    def remove_fields(self, representation, fields_to_remove):
        for field in fields_to_remove:
            representation.pop(field, None)
        return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class GlampForTouristSerializer(GlampSerializer):
    is_active = serializers.BooleanField(required=False, write_only=True)
    is_hidden = serializers.BooleanField(required=False, write_only=True)
    is_verified = serializers.BooleanField(required=False, write_only=True)
    is_approved = serializers.BooleanField(required=False, write_only=True)
    premium_level = serializers.IntegerField(required=False, write_only=True)
    priority = serializers.FloatField(required=False, write_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and hasattr(request.user, "role") and request.user.role == Role.TOURIST:
            fields_to_remove = ["is_active", "is_hidden", "is_verified", "is_approved", "premium_level", "priority"]
            representation = self.remove_fields(representation, fields_to_remove)
        return representation


class GlampForOwnerSerializer(GlampSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and hasattr(request.user, "role") and request.user.role == Role.OWNER:
            fields_to_remove = ["priority"]
            representation = self.remove_fields(representation, fields_to_remove)
        return representation

    def validate(self, attrs):
        if self.context["request"].user.role == Role.OWNER:
            attrs.pop("priority", None)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if self.context["request"].user.role == Role.OWNER:
            validated_data.pop("priority", None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if self.context["request"].user.role == Role.OWNER:
            validated_data.pop("priority", None)
        return super().create(validated_data)


class GlampForManagerSerializer(GlampSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and hasattr(request.user, "role") and request.user.role == Role.MANAGER:
            fields_to_remove = ["priority"]
            representation = self.remove_fields(representation, fields_to_remove)
        return representation

    def validate(self, attrs):
        if self.context["request"].user.role == Role.OWNER:
            attrs.pop("priority", None)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if self.context["request"].user.role == Role.OWNER:
            validated_data.pop("priority", None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if self.context["request"].user.role == Role.OWNER:
            validated_data.pop("priority", None)
        return super().create(validated_data)


class GlampByCategorySerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    glamp_type = serializers.IntegerField(
        required=True, validators=[validate_type]
    )
    name = serializers.CharField(required=True, max_length=225)
    capacity = serializers.IntegerField(required=True, min_value=1)
    status = serializers.IntegerField(
        required=True, validators=[validate_status]
    )
    description = serializers.CharField(required=True, max_length=5000)
    street = serializers.CharField(required=True, max_length=225)
    number_of_bedrooms = serializers.IntegerField(required=True)
    number_of_beds = serializers.IntegerField(required=True)
    number_of_bathrooms = serializers.IntegerField(required=True)
    price = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[validate_glamp_price],
    )
    thumb = serializers.SerializerMethodField()
    images_list = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    thumb_list = serializers.SerializerMethodField()

    class Meta:
        model = Glamp
        fields = "__all__"

    def validate(self, attrs):
        transliterated_name = unidecode(attrs["name"])
        slug = slugify(transliterated_name)
        validate_slug_glamp(
            slug
        )  # Check that the slug has more than 0 characters.
        attrs["slug"] = slug

        return attrs

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        compressed_image = process_image(image)

        uploaded_images = validated_data.pop("uploaded_images", [])

        glamp_obj = Glamp.objects.create(
            owner=self.context["request"].user,
            image=compressed_image,
            **validated_data
        )
        glamp_obj.slug = f"{glamp_obj.id}-{slugify(unidecode(glamp_obj.name))}"

        for image in uploaded_images:
            compressed_image = process_image(image)
            image_list_obj = ImageList.objects.create(images_list=compressed_image, parent=glamp_obj)
            image_list_obj.thumbs_list = image_list_obj.thumbs_list.url
            image_list_obj.save()

        glamp_obj.thumb = glamp_obj.thumb.url
        glamp_obj.save()

        return glamp_obj

    def update(self, instance, validated_data):
        category = validated_data.pop("category", None)

        if category:
            if isinstance(category, Category):
                instance.category = category
            else:
                instance.category = Category.objects.get(id=category)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        glamp = super().update(instance, validated_data)
        if "name" in validated_data:
            glamp.slug = (
                f"{glamp.id}-{slugify(unidecode(validated_data['name']))}"
            )
            glamp.save()

        return instance

    def get_thumb(self, obj):
        if obj.image:
            from urllib.parse import urljoin

            original_path = os.path.basename(obj.thumb.name)
            thumb_name = upload_to(obj, original_path)
            print(thumb_name)
            print(original_path)

            base_path = thumb_name.split("/")[1:-1]
            thumb_path = settings.IMAGE_ROOT + "/".join(base_path) + settings.THUMB_ROOT + original_path.split("/")[-1]

            print(base_path)
            print(thumb_path)
            return self.context["request"].build_absolute_uri(
                urljoin(settings.MEDIA_URL, thumb_path)
            )

        return None

    def get_thumb_list(self, obj):
        from urllib.parse import urljoin

        thumbs = []
        for image_obj in obj.images_list.all():
            if image_obj.thumbs_list:
                original_path = os.path.basename(image_obj.thumbs_list.name)
                thumb_name = upload_to(image_obj, original_path)

                base_path = thumb_name.split("/")[1:-1]
                thumb_path = settings.IMAGE_ROOT + "/".join(base_path) + settings.THUMB_ROOT + original_path.split("/")[-1]

                thumbs.append(self.context["request"].build_absolute_uri(
                    urljoin(settings.MEDIA_URL, thumb_path)
                ))

        return thumbs if thumbs else None

    def get_images_list(self, obj):
        request = self.context.get("request")
        image_urls = [
            request.build_absolute_uri(image_obj.images_list.url)
            for image_obj in obj.images_list.all()
            if image_obj.images_list
        ]
        return image_urls if image_urls else None


class ActivateGlampSerializer(ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Glamp
        fields = ("is_active",)


class HiddenGlampSerializer(ModelSerializer):
    is_hidden = serializers.BooleanField(required=True)

    class Meta:
        model = Glamp
        fields = ("is_hidden",)


class VerifiedGlampSerializer(ModelSerializer):
    is_verified = serializers.BooleanField(required=True)

    class Meta:
        model = Glamp
        fields = ("is_verified",)


class ApprovedGlampSerializer(ModelSerializer):
    is_approved = serializers.BooleanField(required=True)

    class Meta:
        model = Glamp
        fields = ("is_approved",)


class RatingGlampSerializer(ModelSerializer):
    rating = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=5.0,
    )

    class Meta:
        model = Glamp
        fields = ("rating",)


class PremiumLevelGlampSerializer(ModelSerializer):
    premium_level = serializers.IntegerField(
        required=True,
        validators=[validate_premium_level],
    )

    class Meta:
        model = Glamp
        fields = ("premium_level",)


class PriorityGlampSerializer(ModelSerializer):
    priority = serializers.FloatField(
        required=True,
        min_value=0.0,
        max_value=100.0,
    )

    class Meta:
        model = Glamp
        fields = ("priority",)