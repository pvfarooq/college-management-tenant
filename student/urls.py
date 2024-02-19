from rest_framework.routers import SimpleRouter

from .api.views import LeaveRequestViewSet

router = SimpleRouter()
router.register("leave-requests", LeaveRequestViewSet, basename="leave-requests")

urlpatterns = router.urls
