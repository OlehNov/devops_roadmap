from django.db import models


class EventlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using("eventlog")

    def create(self, **kwargs):
        return super().using("eventlog").create(**kwargs)
