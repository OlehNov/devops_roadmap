from rest_framework.routers import DefaultRouter

from glamps.views import GlampViewSet


router = DefaultRouter()
router.register("", GlampViewSet, basename="glamp")

urlpatterns = [] + router.urls
