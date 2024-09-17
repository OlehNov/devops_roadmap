from django.urls import path
from tourists.views import (
    TouristProfileListCreateAPIView,
    TouristProfileRetrieveUpdateDestroyAPIView,
    CurrentUserProfileRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('tourists/', TouristProfileListCreateAPIView.as_view(),),
    path('current-user/', CurrentUserProfileRetrieveUpdateDestroyAPIView.as_view(), ),
    path('tourists/<int:pk>/', TouristProfileRetrieveUpdateDestroyAPIView.as_view(),),
]
