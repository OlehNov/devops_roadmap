from rest_framework.routers import DefaultRouter
from django.urls import path


from tourists.views import TouristViewSet, ActivateTouristView

router = DefaultRouter()
router.register("", TouristViewSet, basename="tourist")

urlpatterns = [
    path("activate-tourist/<str:token>/", ActivateTouristView.as_view(), name="activate-tourist"),
] + router.urls
