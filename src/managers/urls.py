from rest_framework.routers import DefaultRouter

from managers.views import ManagerModelViewSet


router = DefaultRouter()
router.register("", ManagerModelViewSet, basename="manager")

urlpatterns = [] + router.urls
