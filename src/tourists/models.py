from django.core.exceptions import ValidationError
from django.db import models

from config import settings
from users.models import User
from tourists.validators import validate_phone, validate_birthday


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Tourist(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    def clean(self):
        if self.phone:
            try:
                validate_phone(self.phone)
            except ValidationError as e:
                if settings.DEBUG:
                    raise ValidationError({'phone': e})
                else:
                    raise ValidationError({'phone': "Validation error. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."})
        if self.birthday:
            try:
                validate_birthday(self.birthday)
            except ValidationError as e:
                if settings.DEBUG:
                    raise ValidationError({'birthday': e})
                else:
                    raise ValidationError({'birthday': "Validation error. The date should be specified in the format YYYY-MM-DD"})
