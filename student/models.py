from django.db import models

from academic.models import Course, Department, Stream
from core.exceptions import DateOrderViolationError
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
        self.validate_date_order("discontinued_date")
        self.validate_date_order("course_completion_date")
        self.validate_date_order("dismissed_date")

    def validate_date_order(self, field_name):
        enrolled_date = getattr(self, "enrolled_date", None)
        field_value = getattr(self, field_name, None)

        if enrolled_date and field_value and field_value > enrolled_date:
            raise DateOrderViolationError(
                input_date=field_value,
                error_detail=f"'{field_name}' cannot be greater than the 'enrolled_date'",
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
