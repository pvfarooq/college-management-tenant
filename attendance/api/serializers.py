from rest_framework import serializers

from ..models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        exclude = ["created_at", "updated_at"]
