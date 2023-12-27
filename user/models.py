from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole

class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    @property
    def role(self) -> UserRole:
        """Return the user's role."""

        if self.is_superuser:
            return UserRole.ADMIN
        elif self.is_student:
            return UserRole.STUDENT
        elif self.is_faculty:
            return UserRole.FACULTY
