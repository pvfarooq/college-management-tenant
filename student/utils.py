from django.db.models import Max

from .models import Student


def generate_admission_number() -> int:
    """
    Generate a unique admission number for a student.
    Fetches the highest admission number and increments it by 1.
    """

    max_admission_number = Student.objects.aggregate(Max("admission_num"))
    return (max_admission_number["admission_num__max"] or 0) + 1
