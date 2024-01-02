from django.db.models.signals import pre_save
from django.dispatch import receiver

from student.models import Student
from student.utils import generate_admission_number


@receiver(pre_save, sender=Student)
def set_admission_number(sender, instance, **kwargs):
    if not instance.admission_num:
        print("--> set_admission_number")
        instance.admission_num = generate_admission_number()
