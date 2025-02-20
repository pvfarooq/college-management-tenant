# Generated by Django 4.2.8 on 2024-01-04 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("academic", "0001_initial"),
        ("student", "0001_initial"),
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentpenalty",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="student.student"
            ),
        ),
        migrations.AddField(
            model_name="coursefee",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="academic.course"
            ),
        ),
        migrations.AddIndex(
            model_name="studentpenaltypayment",
            index=models.Index(fields=["payment_mode"], name="penalty_pay_mode_idx"),
        ),
        migrations.AddIndex(
            model_name="studentpenalty",
            index=models.Index(
                fields=["student", "is_paid"], name="student_penalty_idx"
            ),
        ),
    ]
