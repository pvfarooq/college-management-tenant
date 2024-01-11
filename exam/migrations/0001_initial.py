# Generated by Django 4.2.8 on 2024-01-11 06:27

import core.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("academic", "0003_subject"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExamType",
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
                (
                    "name",
                    models.CharField(
                        help_text="Exam type (e.g Internal)", max_length=50, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Exam",
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
                ("exam_date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("venue", models.CharField(max_length=50)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="academic.course",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="academic.department",
                    ),
                ),
                (
                    "exam_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exams",
                        to="exam.examtype",
                    ),
                ),
                (
                    "stream",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="academic.stream",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="academic.subject",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["batch", "semester"], name="exam_exam_batch_506ed3_idx"
                    )
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="exam",
            constraint=models.UniqueConstraint(
                fields=(
                    "batch",
                    "semester",
                    "subject",
                    "exam_date",
                    "start_time",
                    "end_time",
                ),
                name="unique_exam",
            ),
        ),
    ]
