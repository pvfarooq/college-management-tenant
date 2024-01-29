from core.router import router

from .api.views import DepartmentViewSet

router.register("departments", DepartmentViewSet)

urlpatterns = router.urls
