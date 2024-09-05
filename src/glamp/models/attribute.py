from django.db.models import CharField, DateTimeField, Model
from django.utils.translation import gettext as _


class Attribute(Model):
    name = CharField(_('Назва Атрибуту'), max_length=225, unique=True)

    created = DateTimeField(_('Створено'), auto_now_add=True)
    updated = DateTimeField(_('Оновлено'), auto_now=True)

    class Meta:
        verbose_name = _('Атрибут')
        verbose_name_plural = _('Атрибут')

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<AttributeModel>: {self.name}'
