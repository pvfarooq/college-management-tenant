# Generated by Django 4.2.8 on 2024-02-19 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("academic", "0004_subject_is_common_alter_subject_course"),
        ("faculty", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutor",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_tutor",
                to="academic.course",
            ),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="stream",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stream_tutor",
                to="academic.stream",
            ),
        ),
    ]
