from rest_framework.serializers import ModelSerializer, ValidationError
from slugify import slugify
from unidecode import unidecode
from categories.validators import validate_slug_category, validate_name_category
from rest_framework import serializers
from users.serializers import UserSerializer
from glamps.models.glamp import Glamp



from categories.models import Category


class CategorySerializer(ModelSerializer):
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

class GlampByCategoryViewSet(ModelSerializer):
    # picture = PictureSerializer(many=True)
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=False
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

