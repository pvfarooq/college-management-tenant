from rest_framework import serializers

from ..models import AlternateTimeTable, Attendance, TimeSlot, TimeTable


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        exclude = ["created_at", "updated_at"]


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        exclude = ["created_at", "updated_at"]


class TimeTableListSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer(read_only=True, many=False)
    course = serializers.CharField(source="course.title", read_only=True)
    stream = serializers.CharField(
        source="stream.title", allow_null=True, required=False, read_only=True
    )
    subject = serializers.CharField(source="subject.title", read_only=True)
    faculty = serializers.CharField(source="faculty.user.get_full_name", read_only=True)

    class Meta:
        model = TimeTable
        exclude = ["created_at", "updated_at"]


class AlternateTimeTableSerializer(serializers.ModelSerializer):
    batch = serializers.IntegerField(read_only=True)
    semester = serializers.IntegerField(read_only=True)

    class Meta:
        model = AlternateTimeTable
        exclude = ["created_at", "updated_at"]


class AlternateTimeTableListSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(source="faculty.user.get_full_name", read_only=True)
    default_timetable = TimeTableListSerializer(read_only=True, many=False)

    class Meta:
        model = AlternateTimeTable
        exclude = ["created_at", "updated_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attendance
        exclude = ["created_at", "updated_at"]


class AttendanceListSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.name", read_only=True)
    faculty = serializers.CharField(source="faculty.user.get_full_name", read_only=True)
    time_slot = TimeSlotSerializer(many=False, read_only=True)

    class Meta:
        model = Attendance
        exclude = ["created_at", "updated_at"]
