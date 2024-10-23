from typing import Iterable
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from users.managers import UserManager
from users.validators import validate_role
from mixins.timestamps import TimestampMixin
from roles.constants import HELP_TEXT_ROLE, ProfileStatus
from users.decorators import role_check


class User(AbstractBaseUser, PermissionsMixin, TimestampMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, default=None)
    last_name = models.CharField(max_length=255, null=True, default=None)
    role = models.PositiveSmallIntegerField(
        null=True,
        default=None,
        validators=[validate_role],
        help_text=HELP_TEXT_ROLE,
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    class Meta:
        db_table = "user"
        ordering = ("-id",)

    def __str__(self):
        return self.email

    @role_check
    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
