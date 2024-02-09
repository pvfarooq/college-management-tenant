from rest_framework.routers import SimpleRouter

from .api.views import (
    AlternateTimeTableViewSet,
    AttendanceViewSet,
    TimeSlotViewSet,
    TimeTableViewSet,
)

router = SimpleRouter()

router.register("timeslots", TimeSlotViewSet)
router.register("timetables", TimeTableViewSet, basename="timetable")
router.register(
    "alt-timetables", AlternateTimeTableViewSet, basename="alternate-timetable"
)
router.register("", AttendanceViewSet, basename="attendance")

urlpatterns = router.urls
