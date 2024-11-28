from rest_framework.routers import DefaultRouter

from tourists.views import TouristViewSet


router = DefaultRouter()
router.register("", TouristViewSet, basename="tourist")

urlpatterns = [] + router.urls
