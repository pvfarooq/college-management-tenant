from django.db import models

from core.enums import Days
from core.exceptions import (
    DateOrderViolationError,
    DuplicateAlternateTimeTableEntry,
    DuplicateAttendanceEntry,
    DuplicateTimeTableEntry,
    TimeOrderViolationError,
)
from core.fields import BatchYearField, SemesterField
from core.models import BaseModel


class TimeSlot(BaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    def save(self, *args, **kwargs):
        self.validate_time_slot()
        super().save(*args, **kwargs)

    def validate_time_slot(self):
        """
        Validates that the start time is less than the end time.
        """
        if self.start_time >= self.end_time:
            raise TimeOrderViolationError(self.start_time, self.end_time)


class SpecialTimeSlot(TimeSlot):
    """
    Represents a special time slot that overrides the regular time slot for a specific day.
    """

    day = models.CharField(max_length=10, choices=Days.choices())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} - ({self.day})"


class TimeTable(BaseModel):
    batch = BatchYearField()
    semester = SemesterField()
    day = models.CharField(max_length=10, choices=Days.choices())
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    course = models.ForeignKey(
        "academic.Course", on_delete=models.CASCADE, related_name="timetables"
    )
    stream = models.ForeignKey(
        "academic.Stream",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="timetables",
    )
    subject = models.ForeignKey(
        "academic.Subject", on_delete=models.CASCADE, related_name="timetables"
    )
    faculty = models.ForeignKey(
        "faculty.Faculty", on_delete=models.CASCADE, related_name="timetables"
    )

    def __str__(self):
        return f"{self.day} - {self.time_slot} - {self.subject}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "semester", "day", "time_slot"],
                name="unique_timetable",
            )
        ]
        indexes = [
            models.Index(fields=["batch", "semester"], name="batch_semester_index")
        ]

    def save(self, *args, **kwargs):
        self.validate_unique_timetable_entry()
        super().save(*args, **kwargs)

    def validate_unique_timetable_entry(self):
        """
        Validates that only one timetable can exist for a batch, in a semester, day and time slot.
        """
        timetable_count = (
            TimeTable.objects.filter(
                batch=self.batch,
                semester=self.semester,
                day=self.day,
                time_slot=self.time_slot,
            )
            .exclude(pk=self.pk)
            .count()
        )

        if timetable_count > 0:
            raise DuplicateTimeTableEntry()


class AlternateTimeTable(BaseModel):
    """
    Represents an alternate timetable.
    Used when the regular timetable is not applicable or when the faculty is not available.
    If an alternate timetable exists for a particular day and time slot,
    it will be used instead of the regular timetable.
    """

    batch = BatchYearField()
    semester = SemesterField()
    start_date = models.DateField()
    end_date = models.DateField()
    default_timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Alternate for {self.default_timetable}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["default_timetable", "faculty", "start_date", "end_date"],
                name="unique_faculty_alternate_timetable",
            )
        ]

    def save(self, *args, **kwargs):
        self.validate_unique_alternate_timetable()
        self.validate_dates()
        super().save(*args, **kwargs)

    def validate_unique_alternate_timetable(self):
        """
        Validates that only one alternate timetable can exist
        for a timetable within a given date range for a faculty.
        """
        alternate_timetable_count = (
            AlternateTimeTable.objects.filter(
                default_timetable=self.default_timetable,
                faculty=self.faculty,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            )
            .exclude(pk=self.pk)
            .count()
        )

        if alternate_timetable_count > 0:
            raise DuplicateAlternateTimeTableEntry()

    def validate_dates(self):
        """
        Validates that the start date is less than the end date.
        """
        if self.start_date >= self.end_date:
            raise DateOrderViolationError(self.start_date)


class Attendance(BaseModel):
    batch = BatchYearField()
    semester = SemesterField()
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} - {self.student} - {self.time_slot}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["time_slot", "student", "date"], name="unique_attendance"
            )
        ]

    def save(self, *args, **kwargs):
        self.validate_unique_attendance()
        super().save(*args, **kwargs)

    def validate_unique_attendance(self):
        """
        Validates that only one attendance can exist for a student, in a time slot, on a date.
        """
        attendance_count = (
            Attendance.objects.filter(
                time_slot=self.time_slot, student=self.student, date=self.date
            )
            .exclude(pk=self.pk)
            .count()
        )

        if attendance_count > 0:
            raise DuplicateAttendanceEntry()
