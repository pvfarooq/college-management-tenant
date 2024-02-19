from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCollegeAdminOrReadOnly(BasePermission):
    """
    If the user is a college admin, allow all actions. Otherwise, only allow safe methods.
    Does not allow unauthenticated users to access the API.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_college_admin or request.method in SAFE_METHODS
        )


class IsFaculty(BasePermission):
    """
    If the user is a faculty, allow all actions. Otherwise, deny all actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_faculty

    def has_object_permission(self, request, view, obj):
        return obj.faculty == request.user.faculty


class IsTutor(IsFaculty):
    """
    If the user is a class tutor, allow all actions. Otherwise, deny all actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tutor


class IsStudent(BasePermission):
    """
    If the user is a student, allow all actions. Otherwise, deny all actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        return obj.student == request.user.student
