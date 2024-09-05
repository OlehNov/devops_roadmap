from django.core.exceptions import ValidationError
from rest_framework import serializers
from tourists.models import Tourist
from tourists.validators import validate_phone, validate_birthday
from users.models import User


class UserTouristProfileSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='tourist.status', required=False, allow_blank=True)
    phone = serializers.CharField(source='tourist.phone', required=False, allow_blank=True, max_length=15)
    birthday = serializers.DateField(source='tourist.birthday', required=False, allow_null=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'birthday', 'status', 'role']

    def update(self, instance, validated_data):
        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        # Update Tourist profile fields
        tourist_data = validated_data.pop('tourist', {})
        tourist_profile, created = Tourist.objects.get_or_create(user=instance)

        if 'status' in tourist_data:
            tourist_profile.status = tourist_data['status']
        if 'phone' in tourist_data:
            phone = tourist_data['phone']
            try:
                validate_phone(phone)
            except ValidationError as e:
                raise serializers.ValidationError({"phone": str(e)})
            tourist_profile.phone = phone
        if 'birthday' in tourist_data:
            birthday = tourist_data['birthday']
            try:
                validate_birthday(birthday)
            except ValidationError as e:
                raise serializers.ValidationError({"birthday": str(e)})
            tourist_profile.birthday = birthday

        tourist_profile.save()

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['status'] = instance.tourist.status if hasattr(instance, 'tourist') else ''
        ret['phone'] = instance.tourist.phone if hasattr(instance, 'tourist') else ''
        ret['birthday'] = instance.tourist.birthday if hasattr(instance, 'tourist') else ''
        return ret
