from rest_framework.serializers import ModelSerializer, ValidationError
from slugify import slugify
from unidecode import unidecode
from categories.validators import validate_slug_category
from rest_framework import serializers


from categories.models import Category


class CategorySerializer(ModelSerializer):
    name = serializers.CharField(max_length=120, required=True, validators=[validate_slug_category])

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


