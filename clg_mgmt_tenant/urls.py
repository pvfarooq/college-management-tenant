from django.contrib import admin
from django.urls import include, path

from .swagger import urlpatterns as swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    path("attendance/", include("attendance.urls")),
    path("academic/", include("academic.urls")),
] + swagger_urlpatterns
