from django.db import transaction

from eventlogs.constants import OperationType
from eventlogs.models import EventLog


class EventLogMixin:


    def _write_to_db(request, operation_type, operated_object):
        EventLog.objects.create(
            user_id=request.user.id,
            user_email=request.user.email,
            instance=operated_object,
            operation_type=operation_type
        )

    def log_event(self, request, operated_object):

        if self.request.method.upper() == "POST":
            self._write_to_db(request, OperationType.CREATE, operated_object)

        if self.request.method.upper() == "PUT" or request.method == "PATCH":
            self._write_to_db(request, OperationType.UPDATE, operated_object)

        if self.request.method.upper() == "DELETE":
            self._write_to_db(request, OperationType.DELETE, operated_object)
