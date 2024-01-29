from core.router import router

from .api.views import CourseViewSet, DepartmentViewSet

router.register("departments", DepartmentViewSet)
router.register("courses", CourseViewSet)

urlpatterns = router.urls
