from django.core.exceptions import ValidationError

from glamp_owners.constants import VipStatus


def vip_status_validator(value):
    if value not in [status.value for status in VipStatus]:
        raise ValidationError(
            "%(value)s is not a valid status",
            params={"value": value},
        )
