from rest_framework import serializers

from ..models import TimeSlot, TimeTable


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        exclude = ["created_at", "updated_at"]


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        exclude = ["created_at", "updated_at"]


class TimeTableListSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer(read_only=True)
    course = serializers.CharField(source="course.title", read_only=True)
    stream = serializers.CharField(
        source="stream.title", allow_null=True, required=False, read_only=True
    )
    subject = serializers.CharField(source="subject.title", read_only=True)
    faculty = serializers.CharField(source="faculty.user.get_full_name", read_only=True)

    class Meta:
        model = TimeTable
        exclude = ["created_at", "updated_at"]
