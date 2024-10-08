from django.core.exceptions import ValidationError


def eventlog_operation_validator(value):
    if value not in [1, 2, 3]:
        raise ValidationError(f"{value} is not in valid range. Must be 1, 2 or 3")


