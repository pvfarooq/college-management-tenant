from django.db import models
from django.db.models import Q

from core.exceptions import (
    DuplicateExamEntry,
    DuplicateExamResultEntry,
    DuplicateExamTypeEntry,
    TimeOrderViolationError,
)
from core.fields import BatchYearField, SemesterField
from core.models import BaseModel


class ExamType(BaseModel):
    name = models.CharField(
        max_length=50, unique=True, help_text="Exam type (e.g Internal)"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        self.validate_unique_name()
        super().save(*args, **kwargs)

    def validate_unique_name(self):
        """Validates that the exam type name is unique."""

        existing_exam_type = ExamType.objects.filter(
            Q(name=self.name),
        ).exclude(pk=self.pk)

        if existing_exam_type.exists():
            raise DuplicateExamTypeEntry()


class Exam(BaseModel):
    batch = BatchYearField()
    semester = SemesterField()
    exam_type = models.ForeignKey(
        ExamType, on_delete=models.CASCADE, related_name="exams"
    )
    department = models.ForeignKey("academic.Department", on_delete=models.CASCADE)
    course = models.ForeignKey("academic.Course", on_delete=models.CASCADE)
    stream = models.ForeignKey(
        "academic.Stream", on_delete=models.CASCADE, null=True, blank=True
    )
    subject = models.ForeignKey("academic.Subject", on_delete=models.CASCADE)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.exam_type} - {self.subject} - {self.exam_date}"

    class Meta:
        indexes = [
            models.Index(fields=["batch", "semester"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "batch",
                    "semester",
                    "subject",
                    "exam_date",
                    "start_time",
                    "end_time",
                ],
                name="unique_exam",
            )
        ]

    def save(self, *args, **kwargs):
        self.validate_times()
        self.validate_unique_exam()
        super().save(*args, **kwargs)

    def validate_times(self) -> None:
        if self.start_time > self.end_time:
            raise TimeOrderViolationError(
                self.start_time,
                error_detail="Start time cannot be greater than end time",
            )

    def validate_unique_exam(self) -> None:
        """Validates that the exam is unique."""

        existing_exam = Exam.objects.filter(
            Q(batch=self.batch),
            Q(semester=self.semester),
            Q(subject=self.subject),
            Q(exam_date=self.exam_date),
            Q(start_time__gte=self.start_time) | Q(end_time__lte=self.end_time),
        ).exclude(pk=self.pk)

        if existing_exam.exists():
            error_detail = (
                f"An exam for {self.subject} already exists for the semester {self.semester} "
                f"of batch {self.batch} on {self.exam_date} from {self.start_time} to {self.end_time}."
            )
            raise DuplicateExamEntry(error_detail)


class ExamResult(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(
        "student.Student", on_delete=models.CASCADE, related_name="exam_results"
    )
    subject = models.ForeignKey(
        "academic.Subject", on_delete=models.CASCADE, related_name="exam_results"
    )
    faculty = models.ForeignKey(
        "faculty.Faculty", on_delete=models.CASCADE, related_name="published_results"
    )
    batch = BatchYearField()
    semester = SemesterField()
    marks = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=3, null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.exam}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "student", "subject"],
                name="unique_exam_result",
            )
        ]

    def save(self, *args, **kwargs):
        self.validate_unique_exam_result()
        super().save(*args, **kwargs)

    def validate_unique_exam_result(self) -> None:
        """Validates that the exam result is unique."""

        existing_result = ExamResult.objects.filter(
            Q(exam=self.exam),
            Q(student=self.student),
            Q(subject=self.subject),
        ).exclude(pk=self.pk)

        if existing_result.exists():
            error_detail = f"An exam result for student '{self.student}' already exists for the given exam."
            raise DuplicateExamResultEntry(error_detail)
