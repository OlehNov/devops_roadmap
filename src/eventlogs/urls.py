from django.urls import path
from rest_framework.routers import DefaultRouter

from eventlogs.views import EventLogListAPIView, EventLogRetrieveAPIView

router = DefaultRouter()


urlpatterns = [
    path(
        "",
        EventLogListAPIView.as_view(),
        name="eventlogs_list",
    ),
    path("log/<int:id>/",
         EventLogRetrieveAPIView.as_view(),
         name="eventlog"),

] + router.urls
