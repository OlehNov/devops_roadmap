from django.contrib import admin

from glamp_owners.models import GlampOwner


class GlampOwnerAdmin(admin.ModelAdmin):
    list_filter = [
        "id",
        "user",
        "phone",
        "status",
        "is_hidden",
        "is_verified",
        "vip_status",
        "created_at",
        "updated_at"
    ]
    list_display = [
        "id",
        "user",
        "phone",
        "status",
        "is_hidden",
        "is_verified",
        "vip_status",
        "created_at",
        "updated_at"
    ]
    search_fields = [
        "id",
        "user",
        "phone",
        "status",
        "is_hidden",
        "is_verified",
        "vip_status",
        "created_at",
        "updated_at"
    ]


admin.site.register(GlampOwner, GlampOwnerAdmin)
