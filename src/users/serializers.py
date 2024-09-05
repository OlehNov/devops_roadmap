from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserTouristRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True, allow_blank=False)
    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            refresh = RefreshToken.for_user(user)
            return {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }

        msg = 'Must include "username" and "password".'
        raise serializers.ValidationError(msg, code='authorization')


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        get_object_or_404(User, email=value)
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})

        return attrs

    def save(self):
        password = self.validated_data['new_password']
        self.user.set_password(password)
        self.user.save()
        return self.user
