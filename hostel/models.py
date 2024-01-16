from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import BaseModel

from .enums import HostelType


class Hostel(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    block = models.CharField(max_length=10, blank=True, null=True)
    residency_category = models.CharField(max_length=10, choices=HostelType.choices())
    max_capacity = models.PositiveSmallIntegerField(
        help_text="Maximum number of persons that can be accomodated"
    )
    current_occupancy = models.PositiveSmallIntegerField(
        default=0, help_text="Number of persons currently accomodated"
    )
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.name} ({self.residency_category})"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        self.validate_capacity()
        super().clean()

    def validate_capacity(self):
        if self.current_occupancy > self.max_capacity:
            raise ValidationError(
                f"Hostel - {self.name} ({self.residency_category}) is full"
            )

    @property
    def is_full(self):
        """Check if there is vacancy in the hostel."""
        return self.current_occupancy >= self.max_capacity


class Hosteller(BaseModel):
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name="hostellers"
    )
    user = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, related_name="hosteller"
    )
    room = models.CharField(max_length=10, blank=True, null=True)
    joining_date = models.DateField()
    vacated_date = models.DateField(blank=True, null=True)
    is_dismissed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.hostel}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["hostel", "user"], name="unique_hosteller")
        ]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        self.check_hostel_capacity()
        self.validate_unique_hosteller()
        self.validate_gender()
        self.validate_dates()
        super().clean()

    def check_hostel_capacity(self):
        """Check if the hostel has vacancy for the hosteller."""
        if self.hostel.is_full:
            raise ValidationError(f"Hostel - {self.hostel} is full")

    def validate_gender(self):
        """
        Validates the gender of the user before adding them to the hostel.

        Raises:
            ValidationError: If the user's gender is not compatible with the hostel's residency category.
        """
        user_gender = self.user.gender
        hostel_type = HostelType(self.hostel.residency_category)

        if not hostel_type.gender_check(user_gender):
            raise ValidationError(
                f"You cannot add a {user_gender} person to the {hostel_type.name.lower()}'s hostel"
            )

    def validate_unique_hosteller(self):
        """
        Validates if the hosteller is unique based on the user.
        Only one hosteller can be created for a user.
        """
        if Hosteller.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            raise ValidationError(f"{self.user} is already a hosteller")

    def validate_dates(self):
        """
        Validates the dates of the hostel tenant.

        Raises:
            ValidationError: If the vacated date is in the future.
            ValidationError: If the joining date is in the future.
            ValidationError: If the joining date is after the vacated date.
        """
        if self.vacated_date and self.vacated_date > timezone.now().date():
            raise ValidationError("Vacated date cannot be in the future")

        if self.joining_date > timezone.now().date():
            raise ValidationError("Joining date cannot be in the future")

        if self.vacated_date and self.joining_date > self.vacated_date:
            raise ValidationError("Joining date cannot be after vacated date")
