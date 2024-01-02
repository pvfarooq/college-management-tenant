import factory

from academic.tests.factory import CourseFactory, DepartmentFactory, StreamFactory
from student.enums import CourseStatus
from student.models import Student
from user.tests.factory import UserFactory


class StudentFactory(factory.django.DjangoModelFactory):
    """Factory for Student model"""

    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    admission_num = factory.Sequence(lambda n: n + 1)
    batch = factory.Faker("year")
    birthday = factory.Faker("date")
    enrolled_date = factory.Faker("date")
    department = factory.SubFactory(DepartmentFactory)
    course = factory.SubFactory(CourseFactory)
    stream = factory.SubFactory(StreamFactory)
    course_status = factory.Faker(
        "random_element", elements=[e.value for e in CourseStatus]
    )
    course_completion_date = None
    discontinued_date = None
    dismissed_date = None
