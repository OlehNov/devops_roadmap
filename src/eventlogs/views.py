from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from eventlogs.models import EventLog
from eventlogs.serializers import EventLogSerializer
from roles.permissions import RoleIsAdmin


class EventLogListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer


class EventLogRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventLogSerializer

    def get_queryset(self):
        return EventLog.objects.filter(id=self.kwargs.get('id'))