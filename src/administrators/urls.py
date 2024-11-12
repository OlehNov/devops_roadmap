from rest_framework.routers import DefaultRouter

from administrators.views import AdministratorModelViewSet


router = DefaultRouter()
router.register("", AdministratorModelViewSet, basename="administrators")

urlpatterns = [] + router.urls
