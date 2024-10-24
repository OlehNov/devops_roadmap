from django.urls import path

from glamp_owners.views import (
    GlampOwnerRegisterView,
    GlampOwnerListAPIView,
    GlampOwnerRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path(
        "glampowner-register/", GlampOwnerRegisterView.as_view(), name="glampowner_register"
    ),
    path("", GlampOwnerListAPIView.as_view()),
    path("<int:glampowner_id>/", GlampOwnerRetrieveUpdateDestroyAPIView.as_view()),
]
