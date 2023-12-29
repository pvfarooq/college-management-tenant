import factory

from core.enums import AttendanceMode
from core.models import CollegeSettings


class CollegeSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CollegeSettings

    attendance_mode = factory.Faker(
        "random_element", elements=[e.value for e in AttendanceMode]
    )
    max_course_change_window_days = factory.Faker("pyint", min_value=1, max_value=30)
