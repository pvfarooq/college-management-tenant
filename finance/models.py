from django.db import models
from django.utils import timezone

from academic.models import Course
from core.exceptions import DateOrderViolationError, PaymentFieldRequired
from core.models import BaseModel
from student.models import Student

from .enums import PaymentMode


class CourseFee(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField(
        help_text="The start date for the validity of this fee."
    )
    valid_to = models.DateField(help_text="The end date for the validity of this fee.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course} - Fee: {self.fee}"

    def save(self, *args, **kwargs):
        self.clean()
        if timezone.now().date() > self.valid_to:
            self.is_active = False
        super().save(*args, **kwargs)

    def clean(self):
        if self.valid_from > self.valid_to:
            raise DateOrderViolationError(
                input_date=self.valid_from,
                error_detail="'valid_from' date cannot be greater than 'valid_to' date.",
            )
        super().clean()


class StudentPenalty(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - Amount: {self.amount}"

    class Meta:
        verbose_name_plural = "Student Penalties"
        indexes = [
            models.Index(fields=["student", "is_paid"], name="student_penalty_idx"),
        ]


class StudentPenaltyPayment(BaseModel):
    penalty = models.ForeignKey(StudentPenalty, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices())
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    txn_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Transaction ID for electronic payments.",
    )
    reference_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Reference number for challan payments.",
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} - Amount: {}".format(self.penalty.student, self.paid_amount)

    class Meta:
        indexes = [
            models.Index(
                fields=["payment_mode"],
                name="penalty_pay_mode_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.payment_mode in PaymentMode.online_payment_modes() and not self.txn_id:
            raise PaymentFieldRequired(
                payment_mode=self.payment_mode,
                error_detail="Transaction ID is required for electronic payments.",
            )

        if self.payment_mode == PaymentMode.CHALLAN.value and not self.reference_number:
            raise PaymentFieldRequired(
                payment_mode=self.payment_mode,
                error_detail="Reference number is required for challan payments.",
            )
