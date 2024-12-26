from django.core.exceptions import ValidationError

from roles.constants import ProfileStatus


def validate_profile_status(value):
    if value not in [status.value for status in ProfileStatus]:
        raise ValidationError(
            "%(value)s is not a valid status for profile",
            params={"value": value},
        )
