from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CharField, DateTimeField, FloatField, Model
from django.utils.translation import gettext as _


class Address(Model):
    street = CharField(_('Вулиця'), max_length=255, null=False, blank=False)
    house = CharField(_('Будинок'), max_length=255, null=False, blank=False)
    apartment = CharField(
        _('Апартаменти'), max_length=25, null=True, blank=True
    )
    city = CharField(_('Mісто'), max_length=255, null=False, blank=False)
    region = CharField(_('Oбласть'), max_length=255, null=True, blank=True)

    latitude = FloatField(
        _('Широта'),
        default=0.0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True,
        blank=True,
    )
    longitude = FloatField(
        _('Довгота'),
        default=0.0,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True,
        blank=True,
    )

    created = DateTimeField(_('Створено'), auto_now_add=True)
    updated = DateTimeField(_('Оновлено'), auto_now=True)

    class Meta:
        verbose_name = _('Адреса')
        verbose_name_plural = _('Адреса')

    def __str__(self) -> str:
        return f'Mісто {self.city}, {self.region} Oбласть'

    def __repr__(self) -> str:
        return f'<AddressModel>: {self.street}'
