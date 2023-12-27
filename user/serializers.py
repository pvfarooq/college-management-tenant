from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JWTTokenSerializer,
)


class TokenObtainPairSerializer(JWTTokenSerializer):
    """The custom serializer used to obtain a JSON web token."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        return token
