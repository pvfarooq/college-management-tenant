import factory

from academic.models import CourseSyllabus

from .course import CourseFactory


class CourseSyllabusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CourseSyllabus

    course = factory.SubFactory(CourseFactory)
    attachment = factory.django.FileField(filename="cse_syllabus_2020.pdf")
