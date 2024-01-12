from django.db import models
from django.utils import timezone

from core.exceptions import DateOrderViolationError, DuplicateAssignmentResult
from core.fields import BatchYearField, SemesterField
from core.models import BaseModel


class Assignment(BaseModel):
    title = models.CharField(max_length=100)
    batch = BatchYearField()
    semester = SemesterField()
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE)
    subject = models.ForeignKey("academic.Subject", on_delete=models.CASCADE)
    due_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.validate_due_date()
        super().save(*args, **kwargs)

    def validate_due_date(self):
        if self.due_date < timezone.now().date():
            raise DateOrderViolationError(
                self.due_date, "Due date cannot be in the past"
            )


class AssignmentResult(BaseModel):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE)
    batch = BatchYearField()
    semester = SemesterField()
    submitted_date = models.DateField()
    marks = models.PositiveIntegerField()

    def __str__(self):
        return self.assignment.title + " - " + self.student.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"], name="unique_assignment_result"
            )
        ]

    def save(self, *args, **kwargs):
        self.validate_submitted_date()
        self.unique_assignment_result()
        super().save(*args, **kwargs)

    def validate_submitted_date(self):
        if self.submitted_date > timezone.now().date():
            raise DateOrderViolationError(
                self.submitted_date, "Submitted date cannot be in the future"
            )

    def unique_assignment_result(self):
        if (
            AssignmentResult.objects.filter(
                assignment=self.assignment, student=self.student
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise DuplicateAssignmentResult()
