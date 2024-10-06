import re
from datetime import datetime, date

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_birthday(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d').date()

    age = (date.today() - value).days // 365

    if value > date.today():
        raise serializers.ValidationError("The date of birth cannot be in the future.")
    if age < 18:
        raise serializers.ValidationError("You must be over the age of 18.")
    if age > 125:
        raise serializers.ValidationError("You can't be more than 125 years old.")
    return value


def validate_phone(value):
    phone_pattern = re.compile(r"^\+\d{9,15}$")
    if not phone_pattern.match(value):
        raise ValidationError(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    return value


def validate_first_name(first_name):
    if len(first_name) < 2:
        raise ValidationError(
            "The first name must have more than two characters."
        )

    if re.match(r"^[A-Za-zА-Яа-я'’]+$", first_name) is None:
        raise ValidationError(
            "The first name must not contain digits or special characters."
        )

    return first_name

def validate_last_name(last_name):
    if len(last_name) < 2:
        raise ValidationError(
            "The last name must have more than two characters."
        )

    if re.match(r"^[A-Za-zА-Яа-я'’]+$", last_name) is None:
        raise ValidationError(
            "The last name must not contain digits or special characters."
        )

    return last_name
