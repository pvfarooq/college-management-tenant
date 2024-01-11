from django.test import TestCase

from ..factory import ExamFactory


class ExamTestCase(TestCase):
    def setUp(self):
        self.exam = ExamFactory()

    def test_str_representation(self):
        self.assertEqual(
            str(self.exam),
            f"{self.exam.exam_type} - {self.exam.subject} - {self.exam.exam_date}",
        )

    def test_create_exam_without_stream(self):
        exam = ExamFactory(stream=None)
        self.assertEqual(exam.stream, None)

    def test_start_time_greater_than_end_time(self):
        with self.assertRaises(Exception) as cm:
            ExamFactory(start_time="12:00", end_time="10:00")

        self.assertEqual(
            str(cm.exception),
            "Start time cannot be greater than end time (code: time_order_violation)",
        )

    def test_unique_exam(self):
        with self.assertRaises(Exception) as cm:
            ExamFactory(
                batch=self.exam.batch,
                semester=self.exam.semester,
                subject=self.exam.subject,
                exam_date=self.exam.exam_date,
                start_time=self.exam.start_time,
                end_time=self.exam.end_time,
            )

        self.assertEqual(
            str(cm.exception),
            (
                f"An exam for {self.exam.subject} already exists "
                f"for the semester {self.exam.semester} of batch {self.exam.batch} on "
                f"{self.exam.exam_date} from {self.exam.start_time} to {self.exam.end_time}. "
                f"(code: duplicate_exam_entry)"
            ),
        )
