# Generated by Django 4.2.8 on 2024-01-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0003_remove_studentpenalty_paid_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentpenaltypayment",
            name="paid_amount",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
