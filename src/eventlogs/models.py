from django.db import models

from eventlogs.managers import EventlogManager


class EventLog(models.Model):
    user_id = models.IntegerField(null=True, default=None)
    user_email = models.EmailField(null=True, default=None)
    instance = models.TextField(
        default=None,
        null=True,
    )
    operation_type = models.SmallIntegerField(null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = EventlogManager()

    class Meta:
        db_table = "eventlog"
        ordering = ("-id",)
        # managed = False
