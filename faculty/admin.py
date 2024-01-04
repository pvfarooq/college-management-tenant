from django.contrib import admin

from .models import Faculty, FacultyRole, Tutor

admin.site.register(FacultyRole)
admin.site.register(Faculty)
admin.site.register(Tutor)
