from django.contrib import admin

from .models import Course, Department, Stream

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Stream)
