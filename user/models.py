from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from core.enums import Gender

from .enums import UserRole


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=Gender.choices())

    @property
    def role(self) -> UserRole:
        """Return the user's role."""

        if self.is_superuser:
            return UserRole.ADMIN
        elif self.is_student:
            return UserRole.STUDENT
        elif self.is_faculty:
            return UserRole.FACULTY

    def generate_password_reset_link(self) -> str:
        """Generate a password reset link for the user."""
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = PasswordResetTokenGenerator().make_token(self)
        reset_url = reverse("reset_password", kwargs={"uidb64": uidb64, "token": token})
        return f"http://localhost:8000{reset_url}"

    def validate_password_reset_token(self, token: str) -> bool:
        """Validate the password reset link."""
        return PasswordResetTokenGenerator().check_token(self, token)

    @classmethod
    def get_user_from_uidb64(cls, uidb64: str) -> Optional["User"]:
        """Return the user from the uidb64."""
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            return cls.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, cls.DoesNotExist):
            return None
