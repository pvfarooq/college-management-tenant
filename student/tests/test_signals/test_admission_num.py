from django.test import TestCase

from student.models import Student

from ..factory import StudentFactory


class SetAdmissionNumberlTestCase(TestCase):
    def test_set_admission_number_signal_creates_admission_number(self):
        student = StudentFactory(admission_num=None)
        student.save()
        updated_student = Student.objects.get(pk=student.pk)
        self.assertIsNotNone(updated_student.admission_num)

    def test_set_admission_number_signal_does_not_modify_existing_admission_number(
        self,
    ):
        student_with_admission_num = StudentFactory(admission_num=12345)
        student_with_admission_num.save()
        updated_student_with_admission_num = Student.objects.get(
            pk=student_with_admission_num.pk
        )
        self.assertEqual(updated_student_with_admission_num.admission_num, 12345)
