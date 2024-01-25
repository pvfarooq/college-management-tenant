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
