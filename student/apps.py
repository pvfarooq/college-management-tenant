from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "student"

    def ready(self):
        import student.signals.admission_num  # noqa: F401
        import student.signals.pre_leave_request_delete  # noqa: F401
