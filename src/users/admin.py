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
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    ]
    list_display = [
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
    search_fields = [
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

    def save_model(
        self, request: Any, obj: Any, form: Any, change: Any
    ) -> None:
        if change:
            previous_role = User.objects.get(id=obj.id)

            if previous_role.role != obj.role:
                match previous_role:
                    case Role.ADMIN:
                        admin_instance = Administrator.objects.filter(user=obj)
                    case Role.TOURIST:
                        tourist_instance = Tourist.objects.filter(user=obj)
                    case Role.OWNER:
                        print("Removing OWNER related object")

            match obj.role:
                case Role.ADMIN:
                    admin_obj, created = Administrator.objects.get_or_create(
                        id=obj.id, user=obj
                    )
                    admin_obj.save()

                case Role.TOURIST:
                    tourist_obj, created = Tourist.objects.get_or_create(
                        id=obj.id, user=obj
                    )
                    tourist_obj.save()

                case Role.OWNER:
                    print('Assigning OWNER related object')

        return super().save_model(request, obj, form, change)
