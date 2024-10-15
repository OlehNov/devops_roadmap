from django.contrib import admin
from administrators.models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    list_filter = [
        "id",
        "user",
        "created_at",
        "updated_at"
    ]
    list_display = [
        "id",
        "user",
        "created_at",
        "updated_at"
    ]
    search_fields = [
        "id",
        "user",
        "created_at",
        "updated_at"
    ]


admin.site.register(Administrator, AdministratorAdmin)
