from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

from owners.validators import vip_status_validator
from users.validators import validate_first_name_last_name
from owners.models import Owner
from tourists.validators import validate_phone
from django.core.exceptions import ValidationError



User = get_user_model()

class OwnerRegistrationSerializer(serializers.ModelSerializer):
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


class OwnerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        source="owner.phone", required=False, allow_blank=True, max_length=15
    )
    status = serializers.IntegerField(
        source="owner.status", required=False, allow_null=True
    )
    is_hidden = serializers.BooleanField(
        source="owner.is_hidden", required=False, default=False
    )
    is_verified = serializers.BooleanField(
        source="owner.is_verified", required=False, default=False
    )
    vip_status = serializers.IntegerField(
        source="owner.vip_status", required=False, allow_null=True
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
        # Update Owner fields
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        # Update Owner profile fields
        owner_data = validated_data.pop("owner", {})
        owner_profile, created = Owner.objects.get_or_create(user=instance)


        if "phone" in owner_data:
            phone = owner_data["phone"]
            try:
                validate_phone(phone)
            except ValidationError as e:
                raise serializers.ValidationError({"phone": str(e)})
            owner_profile.phone = phone

        if "status" in owner_data:
            owner_profile.status = owner_data["status"]
        if "is_hidden" in owner_data:
            owner_profile.is_hidden = owner_data["is_hidden"]
        if "is_verified" in owner_data:
            owner_profile.is_verified = owner_data["is_verified"]
        if "vip_status" in owner_data:
            vip_status = owner_data["vip_status"]
            try:
                vip_status_validator(vip_status)
            except ValidationError as e:
                raise serializers.ValidationError({"vip_status": str(e)})
            owner_profile.vip_status = vip_status

        owner_profile.save()

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["phone"] = instance.owner.phone if hasattr(instance, "owner") else ""
        ret["status"] = instance.owner.status if hasattr(instance, "owner") else None
        ret["is_hidden"] = instance.owner.is_hidden if hasattr(instance, "owner") else False
        ret["is_verified"] = instance.owner.is_verified if hasattr(instance, "owner") else False
        ret["vip_status"] = instance.owner.vip_status if hasattr(instance, "owner") else None

        return ret


class OwnerDeactivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_deleted"]

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get("is_active", False)
        instance.is_deleted = validated_data.get("is_deleted", True)
        instance.save()
        return instance