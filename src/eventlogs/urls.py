from django.urls import path
from rest_framework.routers import DefaultRouter

from eventlogs.views import EventLogListAPIView, EventLogRetrieveAPIView


urlpatterns = [
    path(
        "",
        EventLogListAPIView.as_view(),
        name="eventlogs_list",
    ),
    path("<int:event_id>/",
         EventLogRetrieveAPIView.as_view(),
         name="eventlog"),

]
