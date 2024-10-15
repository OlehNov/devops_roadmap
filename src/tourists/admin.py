from django.contrib import admin

from tourists.models import Tourist


class TouristAdmin(admin.ModelAdmin):
    list_filter = [
        "id",
        "user",
        "status",
        "birthday",
        "phone",
        "created_at",
        "updated_at"
    ]
    list_display = [
        "id",
        "user",
        "status",
        "birthday",
        "phone",
        "created_at",
        "updated_at"
    ]
    search_fields = [
        "id",
        "user",
        "status",
        "birthday",
        "phone",
        "created_at",
        "updated_at"
    ]


admin.site.register(Tourist, TouristAdmin)
