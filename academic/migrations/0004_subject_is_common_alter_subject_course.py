# Generated by Django 4.2.8 on 2024-02-02 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("academic", "0003_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="is_common",
            field=models.BooleanField(
                default=False,
                help_text="Check this if this subject is common for all streams",
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="academic.course",
            ),
        ),
    ]
