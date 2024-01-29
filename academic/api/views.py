from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from academic.models import Department
from user.permissions import IsCollegeAdminOrReadOnly

from .serializers import DepartmentSerializer


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]
