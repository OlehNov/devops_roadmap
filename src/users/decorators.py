from functools import wraps
from django.contrib.auth import get_user_model
from roles.constants import Role, ProfileStatus


def role_check(func):

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        User = get_user_model()
        if User.DoesNotExist:
            return func(instance, *args, **kwargs)

        def __deactivate_profile(model, user_instance):
            profile_instance = model.objects.get(user=user_instance)
            profile_instance.status = ProfileStatus.DEACTIVATED
            profile_instance.save()

        def __activate_profile(model, user_instance):
            profile_instance = model.objects.get(user=user_instance)
            profile_instance.status = ProfileStatus.ACTIVATED
            profile_instance.save()

        user = User.objects.get(id=instance.id)

        if user.role != instance.role:
            match user.role:
                case Role.ADMIN:
                    from administrators.models import Administrator
                    __deactivate_profile(Administrator, instance)

                case Role.TOURIST:
                    from tourists.models import Tourist
                    __deactivate_profile(Tourist, instance)

                case Role.OWNER:
                    from glamp_owners.models import GlampOwner
                    __deactivate_profile(GlampOwner, instance)

        match instance.role:
            case Role.ADMIN:
                from administrators.models import Administrator
                __activate_profile(Administrator, instance)

            case Role.TOURIST:
                from tourists.models import Tourist
                __activate_profile(Tourist, instance)

            case Role.OWNER:
                from glamp_owners.models import GlampOwner
                __activate_profile(GlampOwner, instance)

        return func(instance, *args, **kwargs)

    return wrapper
