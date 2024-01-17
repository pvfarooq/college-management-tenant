from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from .serializers import PasswordResetSerializer, ResetPasswordSerializer


class DeactivateUserView(generics.UpdateAPIView):
    """Deactivates a user account."""

    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    lookup_url_kwarg = "user_id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {"message": "User account deactivated."}, status=status.HTTP_200_OK
        )


class PasswordResetLinkView(APIView):
    """Sends a password reset link to the user's email."""

    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.get(email=email)
        reset_link = user.generate_password_reset_link()
        return Response(
            {"message": "Password reset link sent to email.", "reset_link": reset_link},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """Changes the user's password."""

    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        user = User.get_user_from_uidb64(uidb64)
        if user is None:
            return Response(
                {"message": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user.validate_password_reset_token(token):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                {"message": "Password changed successfully."}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST
        )
