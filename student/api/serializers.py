from rest_framework import serializers

from ..models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = LeaveRequest
        exclude = ["created_at", "updated_at"]


class LeaveRequestListSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source="student.name", read_only=True)
    tutor = serializers.CharField(
        source="tutor.faculty.user.get_full_name", read_only=True
    )

    class Meta:
        model = LeaveRequest
        exclude = ["created_at", "updated_at"]
