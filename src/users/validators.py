import re

from django.core.exceptions import ValidationError

from roles.constants import Role


class NoSpacePasswordValidator:
    def validate(self, password, user=None):
        if " " in password:
            raise ValidationError(
                "The password must not contain spaces.",
                code="password_contains_space",
            )

    def get_help_text(self):
        return "The password must not contain spaces."


class LatinOnlyPasswordValidator:
    def validate(self, password, user=None):
        if re.search(r"[^\x00-\x7F]", password):
            raise ValidationError(
                "The password must contain only Latin characters.",
                code="password_not_latin",
            )

    def get_help_text(self):
        return "The password must contain only Latin characters."


class DigitRequiredPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r"\d", password):
            raise ValidationError(
                "The password must contain at least one digit.",
                code="password_no_digit",
            )

    def get_help_text(self):
        return "Your password must contain at least one digit."


class UpperLowerCasePasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "The password must contain at least one uppercase letter.",
                code="password_no_uppercase",
            )
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "The password must contain at least one lowercase letter.",
                code="password_no_lowercase",
            )

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter and one lowercase letter."


class MaximumLengthValidator:
    def validate(self, password, user=None):
        if len(password) > 255:
            raise ValidationError("The password must contain no more than 255 characters")


def validate_role(value):
    if value not in [role.value for role in Role]:
        raise ValidationError(
            "%(value)s is not a valid role",
            params={"value": value},
        )


def validate_first_name_last_name(value):
    if len(value) < 2:
        raise ValidationError("The name must have more than two characters.")

    if re.match(r"^[A-Za-zА-Яа-яєЄїЇіІ`'ʼ-]+$", value) is None:
        raise ValidationError("The name must not contain digits or special characters.")

    return value
