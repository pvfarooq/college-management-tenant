# Generated by Django 4.2.8 on 2024-02-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_collegesettings_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="collegesettings",
            name="max_attendance_change_window_days",
            field=models.PositiveIntegerField(
                default=2,
                help_text="Maximum days allowed to change attendance after adding it.",
            ),
            preserve_default=False,
        ),
    ]
