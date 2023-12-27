from django.contrib import admin
from django.urls import include, path

from .swagger import urlpatterns as swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
] + swagger_urlpatterns
