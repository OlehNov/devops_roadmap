from django.contrib import admin

from glamps.models import Glamp, Picture


@admin.register(Glamp)
class GlampAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "type_glamp",
        "capacity",
        "status",
        "price",
        "status",
        "street",
        "city",
        "region",
        "latitude",
        "longitude",
        "created_at",
        "updated_at"
    )

admin.site.register(Picture)
