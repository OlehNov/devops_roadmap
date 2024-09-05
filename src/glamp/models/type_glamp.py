from django.db.models import CharField, DateTimeField, Model
from django.utils.translation import gettext as _


class TypeGlamp(Model):
    name = CharField(_('Тип Глемпу'), max_length=220, unique=True)

    created = DateTimeField(_('Створено'), auto_now_add=True)
    updated = DateTimeField(_('Оновлено'), auto_now=True)

    class Meta:
        verbose_name = _('Тип Глемпу')
        verbose_name_plural = _('Типи Глемпу')

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<TypeGlampModel>: {self.name}'
