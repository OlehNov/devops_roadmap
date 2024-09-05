from django.contrib import admin

from glamp.models import (
    Address,
    Attribute,
    AttributeGlamp,
    Category,
    Glamp,
    Picture,
    TypeGlamp
)


class AttributeGlampInLine(admin.StackedInline):
    model = AttributeGlamp
    extra = 0


@admin.register(Glamp)
class GlampAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'type_glamp__name',
        'capacity',
        'status',
        'price',
    )
    inlines = [AttributeGlampInLine]


admin.site.register(Address)
admin.site.register(Attribute)
admin.site.register(AttributeGlamp)
admin.site.register(Picture)
admin.site.register(TypeGlamp)
admin.site.register(Category)
