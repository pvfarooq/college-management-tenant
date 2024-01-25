from core.router import router

from .api.views import TimeSlotViewSet

router.register("timeslots", TimeSlotViewSet)

urlpatterns = router.urls
