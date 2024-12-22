from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from slugify import slugify
from unidecode import unidecode

from addons.mixins.eventlog import EventLogForSerializersMixin
from categories.models import Category
from categories.validators import (validate_name_category,
                                   validate_slug_category)


class CategorySerializer(ModelSerializer, EventLogForSerializersMixin):
    name = serializers.CharField(max_length=120, required=True, validators=[validate_name_category])
    slug = serializers.SlugField(max_length=120, required=False, validators=[validate_slug_category])

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        if not attrs.get("slug") and attrs.get("name"):
            transliterated_name = unidecode(attrs["name"])
            slug = slugify(transliterated_name)
            validate_slug_category(slug)  # Check that the slug has more than 0 characters.
            attrs["slug"] = slug

        slug = attrs.get("slug")
        if slug and Category.objects.filter(slug=slug).exists():
            raise ValidationError(
                {"slug": "Category with this slug already exists."}
            )

        name = attrs.get("name")
        if name and Category.objects.filter(name=name).exists():
            raise ValidationError(
                {"name": "Category with this Name already exists."}
            )

        return attrs

    def create(self, validated_data):
        category = super().create(validated_data)
        request = self.context.get("request")

        if request:
            self.log_event_for_serializer(request=request, validated_data=category)
        return category

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        request = self.context.get("request")

        if request:
            self.log_event_for_serializer(request=request, validated_data=updated_instance)
        return updated_instance
