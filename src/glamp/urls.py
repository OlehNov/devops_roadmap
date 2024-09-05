from django.urls import include, path
from rest_framework.routers import DefaultRouter

from glamp.views import GlampListView

router = DefaultRouter()
router.register('glamp', GlampListView)

urlpatterns = [
    path('', include(router.urls)),
]
