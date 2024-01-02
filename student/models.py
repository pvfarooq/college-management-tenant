from django.core.exceptions import ValidationError
from django.db import models

from academic.models import Course, Department, Stream
from core.fields import BatchYearField
from core.models import BaseModel

from .enums import CourseStatus


class Student(BaseModel):
    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    admission_num = models.PositiveBigIntegerField(unique=True, editable=False)
    batch = BatchYearField()
    birthday = models.DateField()
    enrolled_date = models.DateField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
    )
    course_status = models.CharField(
        max_length=50, choices=CourseStatus.choices(), default=CourseStatus.ENROLLED
    )
    course_completion_date = models.DateField(blank=True, null=True)
    discontinued_date = models.DateField(blank=True, null=True)
    dismissed_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["batch"], name="batch_idx"),
        ]

    def clean(self):
        if self.discontinued_date and self.discontinued_date > self.enrolled_date:
            raise ValidationError(
                "Discontinued date cannot be earlier than enrolled date."
            )

        if (
            self.course_completion_date
            and self.course_completion_date > self.enrolled_date
        ):
            raise ValidationError(
                "Course completion date cannot be earlier than enrolled date."
            )

        if self.dismissed_date and self.dismissed_date > self.enrolled_date:
            raise ValidationError(
                "Dismissed date cannot be earlier than enrolled date."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
