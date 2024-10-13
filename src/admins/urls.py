from django.urls import path
from admins.views import (
    AdminListAPIView,
    AdminRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", AdminListAPIView.as_view()),
    path("<int:admin_id>/", AdminRetrieveUpdateDestroyAPIView.as_view()),
]
