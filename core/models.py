import uuid

from django.db import models

from .enums import AttendanceMode


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

    def __str__(self):
        return "College Settings"


class SemesterSettings(BaseModel):
    semester = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.semester
