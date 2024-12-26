from functools import wraps

from django.contrib.auth import get_user_model
from django.db import transaction

from roles.constants import ProfileStatus, Role


def __deactivate_profile(model, user_instance):
    profile_instance = model.objects.get(
        id=user_instance.id,
        user=user_instance,
    )
    if profile_instance:
        profile_instance.status = ProfileStatus.DEACTIVATED
        profile_instance.save()


def __activate_profile(model, user_instance):
    profile_instance, created = model.objects.get_or_create(
        id=user_instance.id,
        user=user_instance,
    )
    if profile_instance and profile_instance.status != ProfileStatus.ACTIVATED:
        profile_instance.status = ProfileStatus.ACTIVATED
        profile_instance.save()


def role_check(func):

    @wraps(func)
    @transaction.atomic()
    def wrapper(instance, *args, **kwargs):
        User = get_user_model()

        user = User.objects.filter(id=instance.id).first()

        if user is None:
            func(instance, *args, **kwargs)

            match instance.role:

                case Role.TOURIST:
                    from tourists.models import Tourist

                    __activate_profile(Tourist, instance)

                case Role.OWNER:
                    from glamp_owners.models import GlampOwner

                    __activate_profile(GlampOwner, instance)

                case Role.ADMIN:
                    from administrators.models import Administrator

                    __activate_profile(Administrator, instance)

                case Role.MANAGER:
                    from managers.models import GlampManager

                    __activate_profile(GlampManager, instance)

        if user is not None and user.role != instance.role:
            match user.role:

                case Role.TOURIST:
                    from tourists.models import Tourist

                    __deactivate_profile(Tourist, instance)

                case Role.OWNER:
                    from glamp_owners.models import GlampOwner

                    __deactivate_profile(GlampOwner, instance)

                case Role.ADMIN:
                    from administrators.models import Administrator

                    __deactivate_profile(Administrator, instance)

                case Role.MANAGER:
                    from managers.models import GlampManager

                    __deactivate_profile(GlampManager, instance)

        match instance.role:

            case Role.TOURIST:
                from tourists.models import Tourist

                __activate_profile(Tourist, instance)

            case Role.OWNER:
                from glamp_owners.models import GlampOwner

                __activate_profile(GlampOwner, instance)

            case Role.ADMIN:
                from administrators.models import Administrator

                __activate_profile(Administrator, instance)

            case Role.MANAGER:
                from managers.models import GlampManager

                __activate_profile(GlampManager, instance)

        return func(instance, *args, **kwargs)

    return wrapper
