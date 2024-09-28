from django.db import transaction

from eventlogs.constants import OperationType
from eventlogs.models import EventLog


class EventLogMixin:
    def write_to_db(self, request, operation_type, operated_object):
        EventLog.objects.using('eventlogs').create(
            user_id=request.user.id,
            user_email=request.user.email,
            object_type=operated_object,
            operation_type=operation_type
        )

    def log_event(self, request, operated_object):

        if request.method == "POST":
            self.write_to_db(request, OperationType.CREATE, operated_object)

        if request.method == "PUT" or self.request.method == "PATCH":
            self.write_to_db(request, OperationType.UPDATE, operated_object)

        if request.method == "DELETE":
            self.write_to_db(request, OperationType.DELETE, operated_object)
