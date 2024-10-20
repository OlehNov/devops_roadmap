from django.urls import path

from owners.views import (
    OwnerRegisterView,
    OwnerListAPIView,
    OwnerRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path(
        "owner-register/", OwnerRegisterView.as_view(), name="owner_register"
    ),
    path("", OwnerListAPIView.as_view()),
    path("<int:owner_id>/", OwnerRetrieveUpdateDestroyAPIView.as_view()),
]
