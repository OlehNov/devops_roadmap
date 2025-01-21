from rest_framework.routers import DefaultRouter
from django.urls import path

from glamp_owners.views import GlampOwnerViewSet, ActivateGlampOwnerView

router = DefaultRouter()
router.register("", GlampOwnerViewSet, basename="glamp_owner")

urlpatterns = [
    path("activate-glamp_owner/<str:token>/", ActivateGlampOwnerView.as_view(), name="activate-glamp_owner"),
] + router.urls