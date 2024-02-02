from django.contrib import admin

from .models import Course, CourseSyllabus, Department, Stream, Subject

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Stream)
admin.site.register(CourseSyllabus)
admin.site.register(Subject)
