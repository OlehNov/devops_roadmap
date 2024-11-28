from django.contrib.auth import get_user_model
from django.db import models
from addons.mixins.timestamps import TimestampMixin
from roles.constants import HELP_TEXT_PROFILE_STATUS


User = get_user_model()


class GlampManager(TimestampMixin):
    id = models.PositiveIntegerField(primary_key=True)

    first_name = models.CharField(max_length=255, null=True, default=None)
    last_name = models.CharField(max_length=255, null=True, default=None)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        null=True, default=None, help_text=HELP_TEXT_PROFILE_STATUS
    )

    class Meta:
        db_table = "manager"
        ordering = ("-id",)

    def __str__(self) -> str:
        return f"{self.user}"
