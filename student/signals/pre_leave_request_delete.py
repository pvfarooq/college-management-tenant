from django.db.models.signals import pre_delete
from django.dispatch import receiver

from core.exceptions import NonPendingLeaveRequestDeletionError
from student.models import LeaveRequest

from ..enums import LeaveRequestStatus


@receiver(pre_delete, sender=LeaveRequest)
def pre_leave_request_delete(sender, instance, **kwargs):
    if instance.status != LeaveRequestStatus.PENDING.value:
        raise NonPendingLeaveRequestDeletionError
