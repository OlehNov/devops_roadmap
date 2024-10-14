from rest_framework.serializers import ModelSerializer

from eventlogs.models import EventLog


class EventLogSerializer(ModelSerializer):
    class Meta:
        model = EventLog
        fields = "__all__"
