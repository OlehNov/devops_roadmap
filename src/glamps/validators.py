from django.core.exceptions import ValidationError
from glamps.constants import TypeGlamp, GlampStatus

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