# Generated by Django 4.2.8 on 2024-01-04 07:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("title", models.CharField(max_length=255)),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="Course code (e.g. CS101)",
                        max_length=10,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "duration",
                    models.CharField(
                        help_text="Duration of the course (e.g. 3 years", max_length=50
                    ),
                ),
                (
                    "auto_promotion",
                    models.BooleanField(
                        default=False,
                        help_text="True if students are automatically promoted to the next class at the end of the semester",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Department",
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
                ("title", models.CharField(max_length=255)),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="Department code (e.g. CS)",
                        max_length=10,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Stream",
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
                ("title", models.CharField(max_length=255)),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="Stream code (e.g. CS101)",
                        max_length=10,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="academic.course",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="course",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="academic.department"
            ),
        ),
    ]
