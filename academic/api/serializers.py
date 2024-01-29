from rest_framework import serializers

from academic.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ["created_at", "updated_at"]
