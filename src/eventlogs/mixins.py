from eventlogs.constants import OperationType
from eventlogs.models import EventLog


class EventLogMixin:
    """
    Using for logging Create, Update, Delete events ONLY

    Implement by inheriting from EventLogMixin and using log_event method,
    must be implemented after successfully setting changes to main Database

    log_event method takes two arguments: request and object, on which was the operation made
    by checking request method - defining which operation was made and set operation_type value then calling _write_to_db method, which makes new DB raw

    on database, it writes the ID of user, email of user, object on which operation was made, type of the operation and timestamp
    """

    def _write_to_db(self, request, operation_type, operated_object):

        if request.user.is_authenticated:
            user_id = request.user.id
            user_email = request.user.email
        else:
            user_id = None
            user_email = "Anonymous"

        EventLog.objects.create(
            user_id=user_id,
            user_email=user_email,
            instance=operated_object,
            operation_type=operation_type,
        )

    def _validate(self, value):
        if value is None:
            return ValueError(f"{value} is None")
        return value

    def log_event(self, request, operated_object):

        request = self._validate(request)
        operated_object = self._validate(operated_object)
        instance = {
            "instance_id": operated_object.id,
            "instance_class": operated_object.__class__.__name__,
            "request_data": request.data,
        }

        match request.method.upper():
            case "POST":
                operation_type = OperationType.CREATE
            case "PUT" | "PATCH":
                operation_type = OperationType.UPDATE
            case "DELETE":
                operation_type = OperationType.DELETE
            case _:
                raise ValueError(f"Unsupported HTTP method: {request.method}")

        self._write_to_db(request, operation_type, instance)
