from django.urls import path

from tourists.views import (
    TouristListAPIView,
    TouristRetrieveUpdateDestroyAPIView,
    UserTouristRegisterView,
)

urlpatterns = [
    path(
        "tourist-register/", UserTouristRegisterView.as_view(), name="tourist_register"
    ),
    path("", TouristListAPIView.as_view()),
    path("<int:tourist_id>/", TouristRetrieveUpdateDestroyAPIView.as_view()),
]
