from django.urls import path
from rest_framework.routers import DefaultRouter

from glamp_owners.views import (
    ActivateGlampOwnerView,
    GlampOwnerRegisterView,
    GlampOwnerViewSet
)

router = DefaultRouter()
router.register("", GlampOwnerViewSet, basename="glamp_owner")

urlpatterns = [
    path("activate-glamp_owner/<str:token>/", ActivateGlampOwnerView.as_view(), name="activate-glamp_owner"),
    path("register-glamp_owner/", GlampOwnerRegisterView.as_view(), name="register-glamp_owner"),
] + router.urls