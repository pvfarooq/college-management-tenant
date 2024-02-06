from rest_framework.routers import SimpleRouter

from .api.views import TimeSlotViewSet, TimeTableViewSet

router = SimpleRouter()

router.register("timeslots", TimeSlotViewSet)
router.register("timetables", TimeTableViewSet, basename="timetable")

urlpatterns = router.urls
