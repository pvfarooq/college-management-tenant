from django.db import models
from django.utils import timezone

from academic.models import Course, Department, Stream
from core.exceptions import DateOrderViolationError
from core.fields import BatchYearField, SemesterField
from core.models import BaseModel

from .enums import CourseStatus, LeaveRequestStatus


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


class LeaveRequest(BaseModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    tutor = models.ForeignKey(
        "faculty.Tutor",
        on_delete=models.CASCADE,
    )
    semester = SemesterField()
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=LeaveRequestStatus.choices(),
        default=LeaveRequestStatus.PENDING.value,
    )

    def __str__(self):
        return f"{self.student.name} - {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["student"], name="student_idx"),
        ]

    def save(self, *args, **kwargs):
        self.validate_dates()
        super().save(*args, **kwargs)

    @property
    def total_days(self) -> int:
        """Returns the total leave days requested"""
        return (self.to_date - self.from_date).days + 1

    def validate_dates(self):
        """Validates the leave request dates"""

        from_date = self.__parse_date(self.from_date)
        to_date = self.__parse_date(self.to_date)

        if from_date > to_date:
            raise DateOrderViolationError(
                input_date=self.to_date,
                error_detail="'from_date' cannot be greater than 'to_date'",
            )

        if from_date < timezone.now().date():
            raise DateOrderViolationError(
                input_date=self.from_date,
                error_detail="You cannot request leave for past dates",
            )

    def __parse_date(self, date_str: str) -> timezone.datetime.date:
        """Parses the date string to date object"""
        if isinstance(date_str, str):
            return timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            return date_str
