from django.contrib import admin
from administrators.models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    list_filter = ["id", "user", "status", "created_at", "updated_at"]
    list_display = ["id", "user", "status", "created_at", "updated_at"]
    search_fields = ["id", "user", "status", "created_at", "updated_at"]


admin.site.register(Administrator, AdministratorAdmin)
