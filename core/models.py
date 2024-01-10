import uuid

from django.db import models

from .enums import AttendanceMode
from .exceptions import CollegeSettingsAlreadyExists
from .fields import SemesterField


class BaseModel(models.Model):
    """Base model for all models in the project."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Announcement(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.FileField(upload_to="announcements", null=True, blank=True)
    expire_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Holiday(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class CollegeSettings(BaseModel):
    attendance_mode = models.CharField(max_length=20, choices=AttendanceMode.choices())
    max_course_change_window_days = models.PositiveIntegerField()

    _singleton = models.BooleanField(
        default=True,
        editable=False,
        unique=True,
        help_text="This field is used to ensure that only one instance of this model exists.",
    )

    def __str__(self):
        return "College Settings"

    class Meta:
        verbose_name_plural = "College Settings"
        constraints = [
            models.CheckConstraint(
                check=models.Q(_singleton=True),
                name="college_settings_singleton",
            )
        ]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self._state.adding and CollegeSettings.objects.exists():
            raise CollegeSettingsAlreadyExists
        super().clean()


class SemesterSettings(BaseModel):
    semester = SemesterField(unique=True)
    start_month_day = models.DateField()
    end_month_day = models.DateField()

    def __str__(self):
        return f"Semester {self.semester} Settings"

    class Meta:
        verbose_name_plural = "Semester Settings"
