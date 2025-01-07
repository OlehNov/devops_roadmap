from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.forms import ModelForm

from administrators.models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    list_filter = ["id", "user", "status", "created_at", "updated_at"]
    list_display = ["id", "user", "status", "created_at", "updated_at"]
    search_fields = ["id", "user", "status", "created_at", "updated_at"]
    exclude = ["id"]

    def save_model(
        self, request: WSGIRequest, obj: Model, form: ModelForm, change: bool
    ) -> None:
        if obj.user:
            obj.id = obj.user.id

        return super().save_model(request, obj, form, change)


admin.site.register(Administrator, AdministratorAdmin)
