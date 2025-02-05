import re
from datetime import date, datetime

from rest_framework.serializers import ValidationError


def validate_birthday(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if value > date.today():
        raise ValidationError("The date of birth cannot be in the future.")
    elif age < 18:
        raise ValidationError("You must be over the age of 18.")
    elif age > 125:
        raise ValidationError("You can't be more than 125 years old.")

    return value


def validate_phone(value):
    phone_pattern = re.compile(r"^\+\d{9,15}$")
    if not phone_pattern.match(value):
        raise ValidationError(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    return value
