from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey, Model
from django.utils.translation import gettext as _

from glamp.models.attribute import Attribute


class AttributeGlamp(Model):
    attribute = ForeignKey(
        Attribute,
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="attribute",
        verbose_name=_("Атрибут Глемпу"),
    )
    attribute_name = CharField(
        _("Назва Атрибуту"), max_length=225, null=False, blank=False
    )
    glamp = ForeignKey(
        "Glamp",
        on_delete=CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Glamp"),
        related_name="attribute",
    )
    description = CharField(_("Опис"), max_length=255, null=True, blank=True)
    value = CharField(_("Додаткові Дані"), max_length=255, null=True, blank=True)

    created = DateTimeField(_("Створено"), auto_now_add=True)
    updated = DateTimeField(_("Оновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Атрибут Глемпу")
        verbose_name_plural = _("Атрибут Глемпу")

    def __str__(self) -> str:
        return f"{self.attribute_name}"

    def __repr__(self) -> str:
        return f"<AttributeGlampModel>: {self.attribute_name}"
