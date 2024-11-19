from rest_framework.serializers import ModelSerializer, ValidationError
from slugify import slugify
from unidecode import unidecode

from categories.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        if not attrs.get("slug") and attrs.get("name"):
            transliterated_name = unidecode(attrs["name"])
            attrs["slug"] = slugify(transliterated_name)

        slug = attrs.get("slug")
        if slug and Category.objects.filter(slug=slug).exists():
            raise ValidationError({"slug": "A record with this value already exists."})

        return attrs
