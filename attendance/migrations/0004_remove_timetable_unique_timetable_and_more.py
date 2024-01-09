# Generated by Django 4.2.8 on 2024-01-09 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0003_remove_specialtimeslot_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="timetable",
            name="unique_timetable",
        ),
        migrations.AddConstraint(
            model_name="timetable",
            constraint=models.UniqueConstraint(
                fields=("batch", "semester", "day", "time_slot"),
                name="unique_timetable",
            ),
        ),
    ]
