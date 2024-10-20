from django.contrib.auth import get_user_model
from mixins.timestamps import TimestampMixin
from django.db import models
from tourists.validators import validate_phone
from owners.validators import vip_status_validator

User = get_user_model()


class Owner(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(
        max_length=15,
        null=True, blank=True,
        validators=[validate_phone]
    )
    vip_status = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[vip_status_validator]
    )
    status = models.PositiveSmallIntegerField(
        null=True, blank=True
    )


    objects = models.Manager()

    class Meta:
        db_table = "owner"
        ordering = ("-id",)