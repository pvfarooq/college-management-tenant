# Generated by Django 4.2.8 on 2024-01-11 05:15

import core.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0003_leaverequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaverequest",
            name="semester",
            field=core.fields.SemesterField(default=1),
            preserve_default=False,
        ),
    ]
