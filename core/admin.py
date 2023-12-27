from django.contrib import admin

from .models import Announcement, CollegeSettings, Holiday, SemesterSettings

admin.site.register(Announcement)
admin.site.register(CollegeSettings)
admin.site.register(Holiday)
admin.site.register(SemesterSettings)
