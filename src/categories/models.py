from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    Model,
    SlugField,
    TextField,
)
from django.utils.translation import gettext as _


class Category(Model):
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

    created = DateTimeField(_("Created"), auto_now_add=True)
    updated = DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        db_table = "category"
        ordering = ("id",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f"{self.name}"
