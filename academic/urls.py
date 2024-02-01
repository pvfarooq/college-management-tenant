from core.router import router

from .api.views import CourseViewSet, DepartmentViewSet, StreamViewSet, SubjectViewSet

router.register("departments", DepartmentViewSet)
router.register("courses", CourseViewSet)
router.register("streams", StreamViewSet)
router.register("subjects", SubjectViewSet)

urlpatterns = router.urls
