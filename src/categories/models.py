from django.db.models import (
    BooleanField,
    CharField,
    SlugField,
    TextField,
)
from django.utils.translation import gettext as _

from addons.mixins.timestamps import TimestampMixin


class Category(TimestampMixin):
    name = CharField(
        _("Name"),
        max_length=120,
        null=False,
        blank=False,
        unique=True,
    )
    slug = SlugField(
        _("Slug"),
        max_length=120,
        null=False,
        blank=False,
        unique=True,
    )
    title = CharField(_("Title"), max_length=120, null=True, default=None)
    description = TextField(_("Description"), max_length=5000, null=True, default=None)

    is_active = BooleanField(_("Status Active"), default=False)
    is_hidden = BooleanField(_("Status Hidden"), default=False)

    class Meta:
        db_table = "category"
        ordering = ("-id",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f"{self.name}"
