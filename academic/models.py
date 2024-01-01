from django.db import models

from core.models import BaseModel


class Department(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(
        max_length=10,
        help_text="Department code (e.g. CS)",
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Course(BaseModel):
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.CharField(
        max_length=10,
        help_text="Course code (e.g. CS101)",
        unique=True,
        blank=True,
        null=True,
    )
    duration = models.CharField(
        max_length=50, help_text="Duration of the course (e.g. 3 years"
    )
    auto_promotion = models.BooleanField(
        default=False,
        help_text="True if students are automatically promoted to the next class at the end of the semester",
    )

    def __str__(self):
        return self.title


class Stream(BaseModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(
        max_length=10,
        help_text="Stream code (e.g. CS101)",
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title
