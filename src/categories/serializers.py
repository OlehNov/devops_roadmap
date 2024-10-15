from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
