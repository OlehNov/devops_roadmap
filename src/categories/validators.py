import re

from django.core.exceptions import ValidationError


def validate_name_category(value):
    if len(value) < 1:
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

def validate_slug_category(value):
    if len(value) == 0:
        raise ValidationError({"slug": "The slug must have more than zero characters."})

    return value
