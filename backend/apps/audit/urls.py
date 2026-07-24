from rest_framework.routers import DefaultRouter

from .views import ActivityLogViewSet

app_name = "audit"

router = DefaultRouter()
router.register(r"", ActivityLogViewSet, basename="activitylog")

urlpatterns = router.urls
