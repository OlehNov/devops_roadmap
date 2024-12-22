from django.forms import model_to_dict

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
        """
        This method is used to write a new row in DataBase
        Takes 3 arguments - request, operation type(int) and operated_object(object)
        """

        # checking user for authentication and setting variables depending on it
        if request.user.is_authenticated:
            user_id = request.user.id
            user_email = request.user.email
        else:
            user_id = None
            user_email = "Anonymous"

        # creating a new row in database
        EventLog.objects.create(
            user_id=user_id,
            user_email=user_email,
            instance=operated_object,
            operation_type=operation_type,
        )

    # validation for value is not None
    def _validate(self, value):
        if value is None:
            return ValueError(f"{value} is None")
        return value

    def log_event(self, request, operated_object, operation_type=None):
        """
        This method is used for logging event and must be implemented in your code after successfully writing to DB
        Takes two arguments - request and operated_object (object)
        """

        request = self._validate(request)
        operated_object = self._validate(operated_object)
        instance = {
            "instance_id": operated_object.id,
            "instance_class": operated_object.__class__.__name__,
            "request_data": request.data,
        }

        # checking request method and setting operation type depending on it
        if not operation_type:
            match request.method.upper():
                case "POST":
                    operation_type = OperationType.CREATE
                case "PUT" | "PATCH":
                    operation_type = OperationType.UPDATE
                case "DELETE":
                    operation_type = OperationType.DELETE
                case _:
                    raise ValueError(f"Unsupported HTTP method: {request.method}")

        # writing to Database
        self._write_to_db(request, operation_type, instance)


class EventLogForSerializersMixin:

    def _write_to_db(self, request, operation_type, operated_object):
        # checking user for authentication and setting variables depending on it
        if request.user.is_authenticated:
            user_id = request.user.id
            user_email = request.user.email
        else:
            user_id = None
            user_email = "Anonymous"

        # creating a new row in database
        EventLog.objects.create(
            user_id=user_id,
            user_email=user_email,
            instance=operated_object,
            operation_type=operation_type,
        )

    # validation for value is not None
    def _validate(self, value):
        if value is None:
            return ValueError(f"{value} is None")
        return value

    def log_event_for_serializer(self, request, validated_data, operation_type=None):
        """
        Logs an event from serializers.
        """
        request = self._validate(request)

        if validated_data is None:
            raise ValueError("The serializer does not contain an instance for logging.")

        instance = {
            "instance_id": validated_data.id,
            "instance_class": validated_data.__class__.__name__,
            "validated_data": model_to_dict(validated_data),
        }

        if not operation_type:
            if request.method == "POST":
                operation_type = OperationType.CREATE
            elif request.method in ["PUT", "PATCH"]:
                operation_type = OperationType.UPDATE
            else:
                raise ValueError(f"Unsupported HTTP method: {request.method}")

        self._write_to_db(request, operation_type, instance)