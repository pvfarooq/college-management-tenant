from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from academic.models import Course, Department, Stream
from user.permissions import IsCollegeAdminOrReadOnly

from .serializers import (
    CourseListSerializer,
    CourseSerializer,
    DepartmentSerializer,
    StreamListSerializer,
    StreamSerializer,
)


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all().order_by("title")

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by("title")

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CourseListSerializer
        return CourseSerializer


class StreamViewSet(ModelViewSet):
    queryset = Stream.objects.all().order_by("title")

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return StreamListSerializer
        return StreamSerializer
