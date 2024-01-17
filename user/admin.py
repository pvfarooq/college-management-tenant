from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Fields", {"fields": ("gender", "is_student", "is_faculty")}),
    )


admin.site.register(User, CustomUserAdmin)
