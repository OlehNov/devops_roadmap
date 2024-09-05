import re

from django.core.exceptions import ValidationError

from roles.constants import Role


class NoSpacePasswordValidator:
    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                "The password must not contain spaces.",
                code='password_contains_space',
            )

    def get_help_text(self):
        return "The password must not contain spaces."


class LatinOnlyPasswordValidator:
    def validate(self, password, user=None):
        if re.search(r'[^\x00-\x7F]', password):
            raise ValidationError(
                "The password must contain only Latin characters.",
                code='password_not_latin',
            )

    def get_help_text(self):
        return "The password must contain only Latin characters."


def validate_role(value):
    if value not in [role.value for role in Role]:
        raise ValidationError(
            '%(value)s is not a valid role',
            params={'value': value},
        )

