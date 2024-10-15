from django.contrib.auth import get_user_model
from django.db import models

from mixins.timestamps import TimestampMixin


User = get_user_model()


class Administrator(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(null=True, default=None)

    objects = models.Manager()

    class Meta:
        db_table = "administrator"
        ordering = ("-id",)

    # def __str__(self):
    #     return str(self.user)
