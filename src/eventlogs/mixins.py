from eventlogs.constants import OperationType
from eventlogs.models import EventLog


class EventLogMixin:
    """
    Using for logging Create, Update, Delete events

    Implement by inheriting from EventLogMixin and using log_event method,
    must be implemented after successfully setting changes to main Database

    log_event method takes two arguments: request and object, on which was the operation made
    by checking request method - defining which operation was made and set operation_type value when calling _write_to_db method, which makes new DB raw

    on database, it writes the ID of user, email of user, object on which operation was made, type of the operation and timestamp
    """

    def _write_to_db(self, request, operation_type, operated_object):

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
