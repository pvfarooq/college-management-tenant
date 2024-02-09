from django.shortcuts import get_object_or_404
from rest_framework import response, status, viewsets

from user.permissions import IsCollegeAdminOrReadOnly, IsFaculty

from ..models import AlternateTimeTable, Attendance, TimeSlot, TimeTable
from .serializers import (
    AlternateTimeTableListSerializer,
    AlternateTimeTableSerializer,
    AttendanceListSerializer,
    AttendanceSerializer,
    TimeSlotSerializer,
    TimeTableListSerializer,
    TimeTableSerializer,
)


class TimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCollegeAdminOrReadOnly]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all().order_by("start_time")


class TimeTableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCollegeAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        batch = request.query_params.get("batch")
        semester = request.query_params.get("semester")

        if not batch or not semester:
            return response.Response(
                {"error": "expected 'batch' and 'semester' in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        batch = self.request.query_params.get("batch")
        semester = self.request.query_params.get("semester")

        if batch and semester:
            return (
                TimeTable.objects.filter(batch=batch, semester=semester)
                .select_related(
                    "time_slot", "course", "stream", "subject", "faculty__user"
                )
                .order_by("batch", "semester")
            )

        return TimeTable.objects.none()

    def get_object(self):
        obj = get_object_or_404(TimeTable, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TimeTableListSerializer
        return TimeTableSerializer


class AlternateTimeTableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCollegeAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        batch = request.query_params.get("batch")
        semester = request.query_params.get("semester")

        if not batch or not semester:
            return response.Response(
                {"error": "expected 'batch' and 'semester' in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        batch = self.request.query_params.get("batch")
        semester = self.request.query_params.get("semester")

        if batch and semester:
            return (
                AlternateTimeTable.objects.filter(batch=batch, semester=semester)
                .select_related("faculty__user", "default_timetable")
                .order_by("batch", "semester")
            )

        return AlternateTimeTable.objects.none()

    def get_object(self):
        obj = get_object_or_404(AlternateTimeTable, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AlternateTimeTableListSerializer
        return AlternateTimeTableSerializer

    def perform_create(self, serializer):
        default_timetable_id = serializer.validated_data.get("default_timetable").id
        default_timetable = TimeTable.objects.get(id=default_timetable_id)
        serializer.save(
            batch=default_timetable.batch, semester=default_timetable.semester
        )


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    The attendance viewset provides the following actions:
    - list: returns a list of attendance records. (faculty)
    - create: creates a new attendance record. (faculty)
    - retrieve: returns a single attendance record. (faculty)
    - update: updates an attendance record. (faculty)
    - partial_update: partially updates an attendance record. (faculty)
    - destroy: deletes an attendance record not more than n days old. (faculty)
    """

    permission_classes = [IsFaculty]

    def list(self, request, *args, **kwargs):
        batch = request.query_params.get("batch")
        semester = request.query_params.get("semester")

        if not batch or not semester:
            return response.Response(
                {"error": "expected 'batch' and 'semester' in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(faculty=self.request.user.faculty)

    def get_queryset(self):
        batch = self.request.query_params.get("batch")
        semester = self.request.query_params.get("semester")
        faculty = self.request.user.faculty

        if batch and semester:
            return (
                Attendance.objects.filter(
                    batch=batch, semester=semester, faculty=faculty
                )
                .select_related("student", "faculty__user")
                .order_by("-date")
            )

        return Attendance.objects.none()

    def get_object(self):
        obj = get_object_or_404(
            Attendance, id=self.kwargs["pk"], faculty=self.request.user.faculty
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AttendanceListSerializer
        return AttendanceSerializer
