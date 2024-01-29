from rest_framework import viewsets

from user.permissions import IsCollegeAdminOrReadOnly

from ..models import TimeSlot
from .serializers import TimeSlotSerializer


class TimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCollegeAdminOrReadOnly]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all().order_by("start_time")
