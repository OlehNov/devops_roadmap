from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

from glamp_owners.validators import vip_status_validator
from users.validators import validate_first_name_last_name
from glamp_owners.models import GlampOwner
from tourists.validators import validate_phone
from django.core.exceptions import ValidationError


User = get_user_model()


class GlampOwnerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )

        validate_first_name_last_name(attrs["first_name"])
        validate_first_name_last_name(attrs["last_name"])

        return attrs


class GlampOwnerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        source="glampowner.phone", required=True, allow_blank=True, max_length=15
    )
    status = serializers.IntegerField(
        source="glampowner.status", required=False, allow_null=True
    )
    is_hidden = serializers.BooleanField(
        source="glampowner.is_hidden", required=False, default=False
    )
    is_verified = serializers.BooleanField(
        source="glampowner.is_verified", required=False, default=False
    )
    vip_status = serializers.IntegerField(
        source="glampowner.vip_status", required=False, allow_null=True
    )
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "status",
            "is_hidden",
            "is_verified",
            "vip_status",
            "role",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def update(self, instance, validated_data):
        # Update User fields
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        # Update GlampOwner profile fields
        glamp_owner_data = validated_data.pop("glampowner", {})
        glamp_owner_profile, created = GlampOwner.objects.get_or_create(user=instance)


        if "phone" in glamp_owner_data:
            phone = glamp_owner_data["phone"]
            try:
                validate_phone(phone)
            except ValidationError as e:
                raise serializers.ValidationError({"phone": str(e)})
            glamp_owner_profile.phone = phone

        if "status" in glamp_owner_data:
            glamp_owner_profile.status = glamp_owner_data["status"]
        if "is_hidden" in glamp_owner_data:
            glamp_owner_profile.is_hidden = glamp_owner_data["is_hidden"]
        if "is_verified" in glamp_owner_data:
            glamp_owner_profile.is_verified = glamp_owner_data["is_verified"]
        if "vip_status" in glamp_owner_data:
            vip_status = glamp_owner_data["vip_status"]
            try:
                vip_status_validator(vip_status)
            except ValidationError as e:
                raise serializers.ValidationError({"vip_status": str(e)})
            glamp_owner_profile.vip_status = vip_status

        glamp_owner_profile.save()

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["phone"] = instance.glampowner.phone if hasattr(instance, "glampowner") else None
        ret["status"] = instance.glampowner.status if hasattr(instance, "glampowner") else None
        ret["is_hidden"] = instance.glampowner.is_hidden if hasattr(instance, "glampowner") else False
        ret["is_verified"] = instance.glampowner.is_verified if hasattr(instance, "glampowner") else False
        ret["vip_status"] = instance.glampowner.vip_status if hasattr(instance, "glampowner") else None

        return ret


class GlampOwnerDeactivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_deleted"]

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get("is_active", False)
        instance.is_deleted = validated_data.get("is_deleted", True)
        instance.save()
        return instance