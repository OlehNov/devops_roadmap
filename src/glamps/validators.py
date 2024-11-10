from django.core.exceptions import ValidationError
from glamps.constants import TypeGlamp

def validate_type(value):
    if value not in [type_glamp.value for type_glamp in TypeGlamp]:
        raise ValidationError(
            "%(value)s is not a valid type",
            params={"value": value},
        )