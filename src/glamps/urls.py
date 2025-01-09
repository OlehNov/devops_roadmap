from rest_framework.routers import DefaultRouter

from glamps.views import GlampByCategoryViewSet, GlampModelViewSet

router = DefaultRouter()
router.register("glamps", GlampModelViewSet, basename="glamp")

router.register(
    r"categories/(?P<category_id>\d+)/glamps",
    GlampByCategoryViewSet,
    basename="glamp-by-category",
)

urlpatterns = [] + router.urls
