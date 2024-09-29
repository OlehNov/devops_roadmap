from rest_framework.routers import DefaultRouter

from glamps.views import GlampListView


router = DefaultRouter()
router.register("", GlampListView, basename="glamp")

urlpatterns = [] + router.urls
