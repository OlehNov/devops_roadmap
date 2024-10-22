from glamp_owners.constants import VipStatus
from django.core.exceptions import ValidationError


def vip_status_validator(value):
    if value is None:
        return

    try:
        value = int(value)
    except ValueError:
        raise ValidationError(f"{value} is not a valid status")

    if value not in [status.value for status in VipStatus]:
        raise ValidationError(
            "%(value)s is not a valid status",
            params={"value": value},
        )