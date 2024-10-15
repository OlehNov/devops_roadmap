from django.urls import path

from administrators.views import (
    AdministratorListAPIView,
    AdministratorRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path("", AdministratorListAPIView.as_view()),
    path(
        "<int:administrator_id>/",
        AdministratorRetrieveUpdateDestroyAPIView.as_view()
    ),
]
