from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.views import ChangePasswordView, DeactivateUserView, PasswordResetLinkView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("deactivate/<user_id>/", DeactivateUserView.as_view(), name="deactivate_user"),
    path("password-reset/", PasswordResetLinkView.as_view(), name="password_reset"),
    path(
        "reset-password/<uidb64>/<token>/",
        ChangePasswordView.as_view(),
        name="reset_password",
    ),
]
