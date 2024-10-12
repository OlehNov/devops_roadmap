from rest_framework.serializers import ModelSerializer
from users.models import User
from admins.models import Admin


class AdminSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
        ]


    def update(self, instance, validated_data):
        # Update User fields
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        admin_profile, created = Admin.objects.get_or_create(user=instance)
        admin_profile.save()

        return instance


class AdminDeactivateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["is_deleted"]

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get("is_active", False)
        instance.is_deleted = validated_data.get("is_deleted", True)
        instance.save()
        return instance
