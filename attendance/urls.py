from rest_framework.routers import SimpleRouter

from .api.views import AlternateTimeTableViewSet, TimeSlotViewSet, TimeTableViewSet

router = SimpleRouter()

router.register("timeslots", TimeSlotViewSet)
router.register("timetables", TimeTableViewSet, basename="timetable")
router.register(
    "alt-timetables", AlternateTimeTableViewSet, basename="alternate-timetable"
)

urlpatterns = router.urls
