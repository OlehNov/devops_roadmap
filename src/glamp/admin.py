from django.contrib import admin

from glamp.models import (
    Glamp,
    Picture,
)


@admin.register(Glamp)
class GlampAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        'type_glamp',
        "capacity",
        "status",
        "price",
        'status',
        'street',
        'city',
        'region',
        'latitude',
        'longitude',
    )


admin.site.register(Picture)
