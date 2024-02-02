from django.db import models

from core.exceptions import SubjectConstraintError
from core.fields import SemesterField
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
        max_length=50, help_text="Duration of the course (e.g. 6 semesters)"
    )
    auto_promotion = models.BooleanField(
        default=False,
        help_text="If checked, students will be automatically promoted to next semester",
    )
    intake = models.PositiveIntegerField(
        help_text="Number of students that can be admitted to this course per batch",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Stream(BaseModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class CourseSyllabus(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to="course/syllabus/")

    def __str__(self):
        return self.course.title


class Subject(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)
    semester = SemesterField()
    credit = models.PositiveIntegerField(blank=True, null=True)
    is_elective = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_common = models.BooleanField(
        default=False, help_text="Check this if this subject is common for all streams"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Validate that either course should be set or is_common should be set, not both.
        """
        if self.course and self.is_common:
            detail = (
                "Either 'course' should be set or 'is_common' should be set, not both."
            )
            raise SubjectConstraintError(error_detail=detail)
        elif not self.course and not self.is_common:
            raise SubjectConstraintError()
        super().clean()
