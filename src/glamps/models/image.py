from django.core.validators import FileExtensionValidator
from django.db.models import CASCADE, FileField, ForeignKey
from django.utils.translation import gettext as _

from addons.mixins.timestamps import TimestampMixin
from glamps.utils import folder_path


class Picture(TimestampMixin):
    pic = FileField(
        _("Picture"),
        upload_to=folder_path,
        max_length=2000,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "bmp",
                    "svg",
                    "webp",
                ]
            )
        ],
    )
    glamp = ForeignKey(
        "Glamp",
        on_delete=CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Glamp"),
        related_name="picture",
    )

    class Meta:
        db_table = "picture"
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    def __str__(self) -> str:
        return f"{self.pic}"

    def __repr__(self) -> str:
        return f"<Picture>: {self.pic}"
