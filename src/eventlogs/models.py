from django.core.exceptions import ValidationError
from django.db import models


class EventLog(models.Model):
    user_id = models.IntegerField(
        null=True,
        default=None
    )
    user_email = models.EmailField(
        null=True,
        default=None
    )

    instance = models.JSONField(
        default=None,
        null=True,
    )

    operation_type = models.SmallIntegerField(
        null=True,
        default=None
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'eventlog'
        ordering = ("-id",)

    def clean_operation_type(self):
        if self.operation_type not in [1, 2, 3]:
            raise ValidationError("operation type must be 1, 2 or 3")
