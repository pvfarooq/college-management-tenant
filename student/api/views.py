from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response, status, viewsets

from user.permissions import IsStudent

from ..enums import LeaveRequestStatus
from ..models import LeaveRequest
from .serializers import LeaveRequestListSerializer, LeaveRequestSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStudent]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LeaveRequestListSerializer
        return LeaveRequestSerializer

    def get_queryset(self):
        return (
            LeaveRequest.objects.select_related("student", "tutor__faculty__user")
            .filter(student=self.request.user.student)
            .order_by("-created_at")
            .order_by("-updated_at")
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == LeaveRequestStatus.PENDING:
            instance.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)

        message = {"detail": "You can only delete pending leave requests."}
        return response.Response(message, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
