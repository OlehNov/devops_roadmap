from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema

from eventlogs.models import EventLog
from eventlogs.serializers import EventLogSerializer


@extend_schema(tags=["eventlog"])
class EventLogListAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    pagination_class = PageNumberPagination


@extend_schema(tags=["eventlog"])
class EventLogRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventLogSerializer
    lookup_url_kwarg = "event_id"

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return EventLog.objects.none()

        if user.is_staff and user.is_superuser:
            return EventLog.objects.get(id=self.kwargs.get("event_id"))

        return EventLog.objects.none()