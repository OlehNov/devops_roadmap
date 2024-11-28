from django.contrib import admin
from managers.models import GlampManager
from roles.constants import Role
from django.db import transaction
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.forms import ModelForm


class ManagerAdmin(admin.ModelAdmin):
    list_filter = ["id", "user", "status", "created_at", "updated_at"]
    list_display = ["id", "user", "status", "created_at", "updated_at"]
    list_display_links = ["id", "user"]
    search_fields = ["id", "user", "status", "created_at", "updated_at"]
    exclude = ["id"]

    @transaction.atomic
    def save_model(
        self, request: WSGIRequest, obj: Model, form: ModelForm, change: bool
    ) -> None:
        if obj.user:
            obj.id = obj.user.id

        return super().save_model(request, obj, form, change)


admin.site.register(GlampManager, ManagerAdmin)
