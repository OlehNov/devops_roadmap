from functools import wraps
from django.contrib.auth import get_user_model
from roles.constants import Role, ProfileStatus


def role_check(func):

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        previous_role = get_user_model().objects.get(id=instance.id)

        if previous_role.role != instance.role:
            match previous_role.role:
                case Role.ADMIN:
                    from administrators.models import Administrator

                    admin_instance = Administrator.objects.get(user=instance)
                    admin_instance.status = ProfileStatus.DEACTIVATED
                    admin_instance.save()

                case Role.TOURIST:
                    from tourists.models import Tourist

                    tourist_instance = Tourist.objects.get(user=instance)
                    tourist_instance.status = ProfileStatus.DEACTIVATED
                    tourist_instance.save()

                case Role.OWNER:
                    from glamp_owners.models import GlampOwner

                    glamp_owner_instance = GlampOwner.objects.get(
                        user=instance
                    )
                    glamp_owner_instance.status = ProfileStatus.DEACTIVATED
                    glamp_owner_instance.save()

        match instance.role:

            case Role.ADMIN:
                from administrators.models import Administrator

                admin_obj, created = Administrator.objects.get_or_create(
                    id=instance.id, user=instance
                )
                admin_obj.status = ProfileStatus.ACTIVATED
                admin_obj.save()

            case Role.TOURIST:
                from tourists.models import Tourist

                tourist_obj, created = Tourist.objects.get_or_create(
                    id=instance.id, user=instance
                )
                tourist_obj.status = ProfileStatus.ACTIVATED
                tourist_obj.save()

            case Role.OWNER:
                from glamp_owners.models import GlampOwner

                owner_obj, created = GlampOwner.objects.get_or_create(
                    id=instance.id, user=instance
                )
                tourist_obj.status = ProfileStatus.ACTIVATED
                owner_obj.save()

        return func(instance, *args, **kwargs)

    return wrapper
