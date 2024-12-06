from rest_framework.routers import DefaultRouter

from glamp_owners.views import GlampOwnerViewSet


router = DefaultRouter()
router.register("", GlampOwnerViewSet, basename="glamp_owners")

urlpatterns = [] + router.urls
