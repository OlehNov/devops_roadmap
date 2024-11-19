import re

from django.core.exceptions import ValidationError


def validate_name_category(value):
    if len(value) < 5:
        raise ValidationError("The name must have more than two characters.")

    if re.match(r"^[A-Za-zА-Яа-яєЄїЇіІ`'ʼ0-9,.:; ]+$", value) is None:
        raise ValidationError(
            "The name must not contain digits or special characters."
        )

    return value
