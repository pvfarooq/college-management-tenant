from django.test import TestCase

from core.exceptions import DuplicateExamResultEntry

from ..factory import ExamResultFactory


class ExamResultTestCase(TestCase):
    def setUp(self):
        self.exam_result = ExamResultFactory()

    def test_str_representation(self):
        self.assertEqual(
            str(self.exam_result),
            f"{self.exam_result.student} - {self.exam_result.exam}",
        )

    def test_exam_result_is_unique(self):
        """Test that the exam result is unique."""
        exam_result = ExamResultFactory()
        with self.assertRaises(DuplicateExamResultEntry):
            ExamResultFactory(
                exam=exam_result.exam,
                student=exam_result.student,
                subject=exam_result.subject,
            )

    def test_create_exam_results_without_grade_and_remarks(self):
        """Test that exam results can be created without grade and remarks."""
        exam_result = ExamResultFactory(grade=None, remarks=None)
        self.assertIsNone(exam_result.grade)
        self.assertIsNone(exam_result.remarks)
