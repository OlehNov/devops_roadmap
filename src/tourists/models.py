from django.contrib.auth import get_user_model
from django.db import models

from addons.mixins.timestamps import TimestampMixin
from roles.constants import HELP_TEXT_PROFILE_STATUS
from roles.validators import validate_profile_status
from tourists.validators import validate_birthday, validate_phone

User = get_user_model()


class Tourist(TimestampMixin):
    id = models.PositiveIntegerField(primary_key=True)

    first_name = models.CharField(max_length=255, null=True, default=None)
    last_name = models.CharField(max_length=255, null=True, default=None)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        null=True,
        default=None,
        validators=[validate_profile_status],
        help_text=HELP_TEXT_PROFILE_STATUS,
    )

    birthday = models.DateField(
        null=True, blank=True, validators=[validate_birthday]
    )
    phone = models.CharField(
        max_length=15, null=True, blank=True, validators=[validate_phone]
    )

    class Meta:
        db_table = "tourist"
        ordering = ("-id",)

    def __str__(self) -> str:
        return f"{self.user}"
