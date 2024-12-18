from django.conf import settings
from django.db import models

db_alias = settings.EVENTLOGS_DB_ALIAS


class EventlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using(db_alias)

    def create(self, **kwargs):
        return super().using(db_alias).create(**kwargs)
