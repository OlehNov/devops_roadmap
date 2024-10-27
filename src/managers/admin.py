from django.contrib import admin
from managers.models import UserManager


class UserManagerAdmin(admin.ModelAdmin):
    list_filter = ["id", "user", "status", "created_at", "updated_at"]
    list_display = ["id", "user", "status", "created_at", "updated_at"]
    search_fields = ["id", "user", "status", "created_at", "updated_at"]


admin.site.register(UserManager, UserManagerAdmin)
