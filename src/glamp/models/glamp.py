from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.utils.translation import gettext as _

from glamp.constants import STATUS
from glamp.models.address import Address
from glamp.models.type_glamp import TypeGlamp

User = get_user_model()


class Glamp(Model):
    uuid = UUIDField(
        unique=True,
        default=uuid4,
        primary_key=True,
        editable=False,
    )

    type_glamp = ForeignKey(
        TypeGlamp,
        on_delete=CASCADE,
        blank=False,
        null=False,
        related_name="glamp",
        verbose_name=_("Тип Глемпу"),
    )

    name = CharField(
        _("Назва Глемпу"), max_length=225, null=False, blank=False, unique=True
    )
    address = ForeignKey(
        Address,
        on_delete=CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Адреса"),
        related_name="address",
    )
    description = CharField(_("Опис"), max_length=5000, null=True, blank=True)
    capacity = PositiveIntegerField(_("Місткість"), validators=[MinValueValidator(1)])
    price = DecimalField(
        _("Ціна"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        help_text=_("Ціна за одну ніч"),
    )
    status = PositiveSmallIntegerField(_("Статус"), help_text=STATUS)

    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Власник"),
        related_name="glamp",
    )

    created = DateTimeField(_("Створено"), auto_now_add=True)
    updated = DateTimeField(_("Оновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Glamp")
        verbose_name_plural = _("Glamp")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<GlampModel>: {self.name}"
