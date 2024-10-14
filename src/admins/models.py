from django.db import models

from users.models import User


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Admin(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
