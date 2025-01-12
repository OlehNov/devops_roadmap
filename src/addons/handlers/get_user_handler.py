from django.contrib.auth import get_user, aget_user


def get_cached_user(request):
    """
    Retrieve the cached user for the given request.

    This function checks if the user is already cached in the request object.
    If not, it fetches the user using `get_user` and stores it in the `_cached_user` attribute
    for future use.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        User: The authenticated user object associated with the request.

    Note:
        This function is synchronous and should be used in synchronous contexts.
    """
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_user(request)
    return request._cached_user


async def aget_cached_user(request):
    """
    Retrieve the asynchronously cached user for the given request.

    This function checks if the user is already cached in the request object.
    If not, it fetches the user asynchronously using `aget_user` and stores it
    in the `_acached_user` attribute for future use.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        User: The authenticated user object associated with the request.

    Note:
        This function is asynchronous and should be used in asynchronous contexts.
    """
    if not hasattr(request, "_acached_user"):
        request._acached_user = await aget_user(request)
    return request._acached_user
