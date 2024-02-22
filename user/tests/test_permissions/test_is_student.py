from django.test import TestCase
from django.test.client import RequestFactory

from faculty.tests.factory import FacultyFactory
from student.tests.factory import StudentFactory
from user.permissions import IsStudent


class IsStudentPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.student_object = StudentFactory()
        self.non_student_object = FacultyFactory()

    def test_has_permission_student_user(self):
        request = self.factory.get("/some-url/")
        request.user = self.student_object.user
        permission = IsStudent()

        self.assertTrue(permission.has_permission(request, None))

    def test_has_permission_non_student_user(self):
        request = self.factory.get("/some-url/")
        request.user = self.non_student_object.user
        permission = IsStudent()

        self.assertFalse(permission.has_permission(request, None))
