from .attendance_edit_window_closed import AttendanceEditWindowClosed  # noqa
from .base import CustomError  # noqa
from .college_settings_exists import CollegeSettingsAlreadyExists  # noqa
from .date_order_violation import DateOrderViolationError  # noqa
from .duplicate_assignment_result import DuplicateAssignmentResult  # noqa
from .duplicate_attendance import DuplicateAttendanceEntry  # noqa
from .duplicate_exam import DuplicateExamEntry  # noqa
from .duplicate_exam_result import DuplicateExamResultEntry  # noqa
from .duplicate_exam_type import DuplicateExamTypeEntry  # noqa
from .duplicate_timetable import DuplicateAlternateTimeTableEntry  # noqa
from .duplicate_timetable import DuplicateTimeTableEntry  # noqa
from .leave_request_update_denied import LeaveRequestUpdateDeniedError  # noqa
from .non_pending_leave_request_delete import (  # noqa
    NonPendingLeaveRequestDeletionError,
)
from .payment_field_required import PaymentFieldRequired  # noqa
from .subject_constraint_error import SubjectConstraintError  # noqa F401
from .time_order_violation import TimeOrderViolationError  # noqa
