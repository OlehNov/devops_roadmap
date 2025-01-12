from django.contrib.auth import get_user, aget_user


def get_cached_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_user(request)
    return request._cached_user


async def aget_cached_user(request):
    if not hasattr(request, "_acached_user"):
        request._acached_user = await aget_user(request)
    return request._acached_user
