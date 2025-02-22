# Generated by Django 4.2.8 on 2024-01-09 04:54

import core.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("student", "0002_initial"),
        ("academic", "0003_subject"),
        ("faculty", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TimeTable",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("batch", core.fields.BatchYearField()),
                ("semester", core.fields.SemesterField()),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("monday", "MONDAY"),
                            ("tuesday", "TUESDAY"),
                            ("wednesday", "WEDNESDAY"),
                            ("thursday", "THURSDAY"),
                            ("friday", "FRIDAY"),
                            ("saturday", "SATURDAY"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timetables",
                        to="academic.course",
                    ),
                ),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timetables",
                        to="faculty.faculty",
                    ),
                ),
                (
                    "stream",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timetables",
                        to="academic.stream",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timetables",
                        to="academic.subject",
                    ),
                ),
                (
                    "time_slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.timeslot",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField()),
                ("batch", core.fields.BatchYearField()),
                ("semester", core.fields.SemesterField()),
                ("is_present", models.BooleanField(default=True)),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="faculty.faculty",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student",
                    ),
                ),
                (
                    "time_slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.timeslot",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AlternateTimeTable",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reason", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "default_timetable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.timetable",
                    ),
                ),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="faculty.faculty",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="timetable",
            constraint=models.UniqueConstraint(
                fields=("batch", "day", "time_slot"), name="unique_timetable"
            ),
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(
                fields=("time_slot", "student", "date"), name="unique_attendance"
            ),
        ),
        migrations.AddConstraint(
            model_name="alternatetimetable",
            constraint=models.UniqueConstraint(
                fields=("default_timetable", "faculty", "start_date", "end_date"),
                name="unique_faculty_alternate_timetable",
            ),
        ),
    ]
