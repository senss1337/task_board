from rest_framework.routers import SimpleRouter

from core.views import UserViewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
