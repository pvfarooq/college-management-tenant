import datetime

from django.core.exceptions import ValidationError
from django.db import models


class BatchYearField(models.IntegerField):
    """An integer field representing a batch year, limited to values between 1980 and the current year + 1."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_year(self, value):
        if value < 1980 or value > datetime.datetime.now().year + 1:
            raise ValidationError(
                f"Batch year must be between 1980 and {datetime.datetime.now().year + 1}"
            )
