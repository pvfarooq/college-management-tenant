import jwt
from django.conf import settings
from django.test import TestCase

from user.serializers import TokenObtainPairSerializer

from ..factory import UserFactory


class TokenObtainPairSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", password="testpassword")

    def test_get_token(self):
        serializer = TokenObtainPairSerializer(
            data={"username": "testuser", "password": "testpassword"}
        )
        serializer.is_valid()
        token = serializer.validated_data.get("access")

        decoded_token = jwt.decode(
            token, settings.SIMPLE_JWT["VERIFYING_KEY"], algorithms=["RS256"]
        )

        self.assertIn("iss", decoded_token)
        self.assertEqual(decoded_token["iss"], "tenant")
        self.assertIn("role", decoded_token)
        self.assertEqual(decoded_token["role"], self.user.role)
