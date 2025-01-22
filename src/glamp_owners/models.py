from django.contrib.auth import get_user_model
from django.db import models

from addons.mixins.timestamps import TimestampMixin
from glamp_owners.validators import vip_status_validator
from tourists.validators import validate_phone

User = get_user_model()


class GlampOwner(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=255, null=True, default=None)
    last_name = models.CharField(max_length=255, null=True, default=None)

    is_hidden = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        default=None,
        validators=[validate_phone],
    )

    vip_status = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None, validators=[vip_status_validator]
    )

    status = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )

    class Meta:
        db_table = "glamp_owner"
        ordering = ("-id",)

    def __str__(self) -> str:
        return f"{self.user}"
