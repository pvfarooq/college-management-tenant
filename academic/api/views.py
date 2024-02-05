from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from academic.models import Course, Department, Stream, Subject
from user.permissions import IsCollegeAdminOrReadOnly

from .serializers import (
    CourseListSerializer,
    CourseSerializer,
    DepartmentSerializer,
    StreamListSerializer,
    StreamSerializer,
    SubjectListSerializer,
    SubjectSerializer,
)


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all().order_by("title")
    filter_backends = [SearchFilter]
    search_fields = ["title", "code"]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().select_related("department").order_by("title")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["department", "auto_promotion"]
    search_fields = ["title", "code"]

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
    queryset = Stream.objects.all().select_related("course").order_by("title")
    filterset_fields = ["course"]

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


class SubjectViewSet(ModelViewSet):
    queryset = (
        Subject.objects.all().select_related("course", "stream").order_by("title")
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["course", "stream", "is_common", "is_elective", "is_lab"]
    search_fields = ["title", "code"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCollegeAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SubjectListSerializer
        return SubjectSerializer
