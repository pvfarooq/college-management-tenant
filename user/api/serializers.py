from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JWTTokenSerializer,
)

from ..models import User


class TokenObtainPairSerializer(JWTTokenSerializer):
    """The custom serializer used to obtain a JSON web token."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        token["gender"] = user.gender
        return token


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist.")
        return email


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=30)
    confirm_password = serializers.CharField(min_length=8, max_length=30)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
