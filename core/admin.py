from django.contrib import admin

from .models import Announcement, CollegeSettings, Holiday, SemesterSettings

admin.site.register(Announcement)
admin.site.register(Holiday)
admin.site.register(SemesterSettings)


class CollegeSettingsAdmin(admin.ModelAdmin):
    exclude = ["_singleton"]


admin.site.register(CollegeSettings, CollegeSettingsAdmin)
