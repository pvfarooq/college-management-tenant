from enum import Enum


class UserRole(str, Enum):
    COLLEGE_ADMIN = "college_admin"
    STUDENT = "student"
    FACULTY = "faculty"
