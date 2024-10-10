from rest_framework.routers import DefaultRouter

from glamps.views import GlampModelViewSet


router = DefaultRouter()
router.register("", GlampModelViewSet, basename="glamp")

urlpatterns = [] + router.urls
