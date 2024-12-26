import re

from django.core.exceptions import ValidationError

from glamps.constants import GlampStatus, TypeGlamp


def validate_type(value):
    if value not in [type_glamp.value for type_glamp in TypeGlamp]:
        raise ValidationError(
            "%(value)s is not a valid type",
            params={"value": value},
        )

def validate_status(value):
    if value not in [status_glamp.value for status_glamp in GlampStatus]:
        raise ValidationError(
            "%(value)s is not a valid status",
            params={"value": value},
        )

def validate_name_glamp(value):
    if len(value) < 3:
        raise ValidationError("The name must have more than one character.")

    if re.match(r"^[A-Za-zА-Яа-яєЄїЇіІґҐ`'ʼ0-9,.:; \"]+$", value) is None:
        raise ValidationError(
            "The name must not contain digits or special characters."
        )

    if bool(re.search(r"[A-Za-zА-Яа-яєЄїЇіІґҐ]", value)) is False:
        raise ValidationError(
            "There must be at least one letter in the name."
        )

    return value

def validate_slug_glamp(value):
    if len(value) == 0:
        raise ValidationError({"slug": "The slug must have more than zero characters."})

    return value