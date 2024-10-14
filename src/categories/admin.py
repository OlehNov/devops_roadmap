from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "name",
        "slug",
        "title",
        "is_active",
        "is_hidden",
        "created",
        "updated",
    )
