from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions", "password"]
    list_filter = [
        "id",
        "email",
        # "first_name",
        # "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "id",
        "email",
        # "first_name",
        # "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_display_links = [
        "id",
        "email",
    ]
    search_fields = [
        "id",
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    ]


admin.site.register(User, UserAdmin)
