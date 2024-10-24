from django.contrib.auth import get_user_model
from django.db import models
from mixins.timestamps import TimestampMixin
from django.conf import settings
from roles.constants import HELP_TEXT_PROFILE_STATUS

User = get_user_model()


class Administrator(TimestampMixin):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        null=True, default=None, help_text=HELP_TEXT_PROFILE_STATUS
    )

    objects = models.Manager()

    class Meta:
        db_table = "administrator"
        ordering = ("-id",)

    def __str__(self):
        return str(self.user)
