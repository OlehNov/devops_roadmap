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
    object_type = models.CharField(max_length=100)

    operation_type = models.SmallIntegerField(
        null=True,
        default=None
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'eventlogs'


