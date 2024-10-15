from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from config import settings
from mixins.timestamps import TimestampMixin
from tourists.validators import validate_birthday, validate_phone


User = get_user_model()


class Tourist(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(
        null=True,
        blank=True,
        validators=[validate_birthday]
    )
    phone = models.CharField(
        max_length=15,
        null=True, blank=True,
        validators=[validate_phone]
    )

    objects = models.Manager()

    class Meta:
        db_table = "tourist"
        ordering = ("-id",)

    def clean(self):
        if self.phone:
            try:
                validate_phone(self.phone)
            except ValidationError as e:
                if settings.DEBUG:
                    raise ValidationError({"phone": e})
                else:
                    raise ValidationError(
                        {
                            "phone": "Validation error. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                        }
                    )
        if self.birthday:
            try:
                validate_birthday(self.birthday)
            except ValidationError as e:
                if settings.DEBUG:
                    raise ValidationError({"birthday": e})
                else:
                    raise ValidationError(
                        {
                            "birthday": "Validation error. The date should be specified in the format YYYY-MM-DD"
                        }
                    )
