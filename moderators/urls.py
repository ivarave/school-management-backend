from rest_framework.routers import DefaultRouter
from .views import ModeratorViewSet

router = DefaultRouter()
router.register(r"", ModeratorViewSet, basename="moderators")

urlpatterns = router.urls
