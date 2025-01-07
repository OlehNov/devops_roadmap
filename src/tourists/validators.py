import re
from datetime import date, datetime

from django.core.exceptions import ValidationError


def validate_birthday(value):
    age = (date.today() - value).days // 365

    if value > date.today():
        raise ValidationError("The date of birth cannot be in the future.")
    if age < 18:
        raise ValidationError("You must be over the age of 18.")
    if age > 125:
        raise ValidationError("You can't be more than 125 years old.")


def validate_phone(value):
    phone_pattern = re.compile(r"^\+\d{9,15}$")
    if not phone_pattern.match(value):
        raise ValidationError(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
