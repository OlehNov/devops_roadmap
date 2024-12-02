from rest_framework.routers import DefaultRouter
from django.urls import path, include

from categories.views import CategoryViewSet, GlampByCategoryViewSet


router = DefaultRouter()
router.register("", CategoryViewSet, basename="categories")

category_router = DefaultRouter()
category_router.register(
    r"(?P<category_id>\d+)/glamps",
    GlampByCategoryViewSet,
    basename="glamp-by-category",
)

urlpatterns = [
    path("", include(router.urls)),

    path("", include(category_router.urls)),
]