from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from eventlogs.models import EventLog
from eventlogs.serializers import EventLogSerializer


class EventLogListAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    pagination_class = PageNumberPagination


class EventLogRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventLogSerializer
    lookup_url_kwarg = "event_id"

    def get_queryset(self):
        return EventLog.objects.get(id=self.kwargs.get("id"))
