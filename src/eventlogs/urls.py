from django.urls import path

from eventlogs.api import EventLogListAPIView, EventLogRetrieveAPIView


urlpatterns = [
    path(
        "",
        EventLogListAPIView.as_view(),
        name="eventlogs_list",
    ),
    path("<int:event_id>/", EventLogRetrieveAPIView.as_view(), name="eventlog"),
]
