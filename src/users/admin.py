from typing import Any
from django.contrib import admin
from django.contrib.auth import get_user_model
from roles.constants import Role
from administrators.models import Administrator
from tourists.models import Tourist


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions", "password"]
    list_filter = [
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    ]
    list_display_links = [
        "id",
        "email",
        "first_name",
        "last_name",
    ]
    search_fields = [
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    ]
