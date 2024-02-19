from django.db import models

from core.fields import BatchYearField
from core.models import BaseModel


class FacultyRole(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Faculty(BaseModel):
    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        "academic.Department",
        on_delete=models.CASCADE,
    )
    faculty_code = models.CharField(max_length=100, unique=True)
    roles = models.ManyToManyField(FacultyRole)
    joining_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()


class Tutor(BaseModel):
    faculty = models.OneToOneField(
        Faculty,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        "academic.Course",
        on_delete=models.CASCADE,
        related_name="course_tutor",
    )
    stream = models.ForeignKey(
        "academic.Stream",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="stream_tutor",
    )
    batch = BatchYearField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.faculty.user.get_full_name()
