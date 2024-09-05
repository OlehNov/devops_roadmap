from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model
)
from django.utils.translation import gettext as _

from glamp.models.attribute_glamp import AttributeGlamp


class Category(Model):
    name = CharField(_('Kатегорія'), max_length=225)
    attribute = ForeignKey(
        AttributeGlamp,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='category',
        verbose_name=_('Aтрибут'),
    )

    created = DateTimeField(_('Створено'), auto_now_add=True)
    updated = DateTimeField(_('Оновлено'), auto_now=True)

    class Meta:
        verbose_name = _('Kатегорія')
        verbose_name_plural = _('Kатегорія')

    def __str__(self) -> str:
        return f'{self.name}: {self.attribute.attribute_name}'

    def __repr__(self) -> str:
        return f'<CategoryModel>: {self.name}'
