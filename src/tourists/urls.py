from django.urls import path
from rest_framework.routers import DefaultRouter

from tourists.views import (
    ActivateTouristView,
    TouristRegisterView,
    TouristViewSet
)

router = DefaultRouter()
router.register("", TouristViewSet, basename="tourist")

urlpatterns = [
    path("activate-tourist/<str:token>/", ActivateTouristView.as_view(), name="activate-tourist"),
    path("register-tourist/", TouristRegisterView.as_view(), name="register-tourist"),
] + router.urls
