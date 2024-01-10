from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


class BatchYearField(models.PositiveSmallIntegerField):
    """An integer field representing a batch year, limited to values between 1980 and the current year + 1."""

    help_text = "The year of the batch, ranging from 1980 to the current year + 1."

    def validate(self, value, model_instance):
        current_year = datetime.now().year
        if value < 1980 or value > current_year + 1:
            raise ValidationError(
                f"Batch year must be between 1980 and {current_year + 1}"
            )
        super().validate(value, model_instance)

    def db_type(self, connection):
        return "smallint"

    def db_check(self, connection):
        return '"batch" >= 1980 AND "batch" <= extract(year from current_date) + 1'

    def check(self, **kwargs):
        if "value" in kwargs:
            self.validate(kwargs["value"])
        return super().check(**kwargs)


class SemesterField(models.PositiveSmallIntegerField):
    """An integer field representing a semester, limited to values between 1 and 10."""

    help_text = "The semester number, of a batch, ranging from 1 to 10."

    def validate(self, value, model_instance):
        if value < 1 or value > 10:
            raise ValidationError("Semester must be between 1 and 10")
        super().validate(value, model_instance)

    def db_type(self, connection):
        return "smallint"

    def db_check(self, connection):
        return '"semester" >= 1 AND "semester" <= 10'

    def check(self, **kwargs):
        if "value" in kwargs:
            self.validate(kwargs["value"])
        return super().check(**kwargs)
