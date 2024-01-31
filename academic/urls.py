from core.router import router

from .api.views import CourseViewSet, DepartmentViewSet, StreamViewSet

router.register("departments", DepartmentViewSet)
router.register("courses", CourseViewSet)
router.register("streams", StreamViewSet)

urlpatterns = router.urls
