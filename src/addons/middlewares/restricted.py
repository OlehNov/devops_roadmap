import re

from asgiref.sync import iscoroutinefunction, markcoroutinefunction, sync_to_async
from functools import partial

from django.conf import settings
from django.contrib.auth import get_user, aget_user
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.status import HTTP_403_FORBIDDEN


def get_cached_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_user(request)
    return request._cached_user


async def auser(request):
    if not hasattr(request, "_acached_user"):
        request._acached_user = await aget_user(request)
    return request._acached_user


class RestrictAccessMiddleware:
    """
    Middleware that restricts access to specific paths or views for users
    who are inactive, deleted, or anonymous.

    This middleware uses the Django settings to dynamically configure restricted areas,
    ensuring only authorized users can access sensitive or protected resources.

    Features:
    - Handles both synchronous and asynchronous requests.
    - Validates the presence of AuthenticationMiddleware to provide `request.user`.
    - Supports dynamic configuration through the `RESTRICTED_AREA` setting.
    """

    sync_capable = True  # Indicates compatibility with synchronous requests.
    async_capable = True  # Indicates compatibility with asynchronous requests.

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware or view in the chain.

        Raises:
            ValueError: If `get_response` is not provided.
        """
        if get_response is None:
            raise ValueError("get_response must be provided.")
        self.get_response = get_response
        self._async_check()  # Detects if the response is asynchronous.
        super().__init__()

    def __repr__(self):
        """
        Generate a string representation of the middleware instance.

        Returns:
            str: The string representation, including the class and `get_response`.
        """
        return "<%s get_response=%s>" % (
            self.__class__.__qualname__,
            getattr(
                self.get_response,
                "__qualname__",
                self.get_response.__class__.__name__,
            ),
        )

    def _async_check(self):
        """
        Check if `get_response` is an asynchronous function.

        If it is, the middleware is marked as async-capable and will handle requests
        asynchronously when needed.
        """
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    def __call__(self, request):
        """
        Handle incoming requests synchronously.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The processed HTTP response.
        """
        if iscoroutinefunction(self):
            # Delegate to the asynchronous call if applicable.
            return self.__acall__(request)

        response = None
        if hasattr(self, "process_request"):
            # Process the request if the method is defined.
            response = self.process_request(request)

        response = response or self.get_response(request)

        if hasattr(self, "process_response"):
            # Process the response if the method is defined.
            response = self.process_response(request, response)

        return response

    async def __acall__(self, request):
        """
        Handle incoming requests asynchronously.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The processed HTTP response.
        """
        response = None
        if hasattr(self, "process_request"):
            # Process the request asynchronously.
            response = await sync_to_async(
                self.process_request,
                thread_sensitive=True,
            )(request)

        response = response or await self.get_response(request)

        if hasattr(self, "process_response"):
            # Process the response asynchronously.
            response = await sync_to_async(
                self.process_response,
                thread_sensitive=True,
            )(request, response)

        return response

    def process_request(self, request):
        """
        Validate and restrict access based on the user's state and request path.

        This method:
        - Ensures `request.user` exists by checking AuthenticationMiddleware.
        - Lazily loads the user (both sync and async).
        - Verifies if the user is anonymous, inactive, or deleted.
        - Compares the request path against restricted areas defined in settings.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse | None: A restricted response if access is denied; otherwise, None.

        Raises:
            ImproperlyConfigured: If AuthenticationMiddleware is not present.
            ValueError: If `RESTRICTED_AREA` is not defined in settings.
        """
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "The Restrict Access Middleware requires the authentication middleware "
                "to be installed. Edit your MIDDLEWARE setting to include "
                "'django.contrib.auth.middleware.AuthenticationMiddleware' "
                "before the RestrictAccessMiddleware."
            )

        # Lazily initialize user and async user for the request.
        request.user = SimpleLazyObject(lambda: get_user(request))
        request.auser = partial(auser, request)

        user = getattr(request, "user", None)

        if (
            not user
            or isinstance(user, AnonymousUser)
            or not user.is_active
            or getattr(user, "is_deleted", False)
        ):
            # Load restricted configuration from settings.
            restricted_area = getattr(settings, "RESTRICTED_AREA", None)
            if not restricted_area:
                raise ValueError("RESTRICTED_AREA must be set")

            restricted_paths = restricted_area.get("PATHS", [])
            restricted_url_patterns = restricted_area.get(
                "URL_PATTERNS",
                [re.compile(f"^{path}.*$").pattern for path in restricted_paths],
            )
            restricted_excluded_paths = restricted_area.get("EXCLUDED_PATHS", [])

            current_path = request.path

            # Check access restrictions.
            response = self.__check_access(
                current_path=current_path,
                restricted_paths=restricted_paths,
                restricted_url_patterns=restricted_url_patterns,
                restricted_excluded_paths=restricted_excluded_paths,
            )
            if response:
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()  # Force JSON rendering for the response.
                print(f"\n{response.data = }")
                return response

    def __check_access(self, current_path, **kwargs):
        """
        Determine if the current path is restricted.

        Args:
            current_path (str): The path of the incoming request.
            **kwargs: Additional arguments containing restricted paths, patterns, and exclusions.

        Returns:
            HttpResponse | None: A restricted response if access is denied; otherwise, None.
        """
        if current_path in kwargs.get("restricted_paths"):
            return self._get_restricted_response()

        for pattern in kwargs.get("restricted_url_patterns"):
            if re.match(pattern, current_path) and current_path not in kwargs.get(
                "restricted_excluded_paths"
            ):
                return self._get_restricted_response()

        return None

    def _get_restricted_response(self):
        """
        Generate a `403 Forbidden` response for restricted access.

        Returns:
            Response: A DRF Response object with a JSON payload indicating access denial.
        """
        return Response(
            {
                "detail": "Access denied. Your account is inactive, deleted, or you are not logged in."
            },
            status=HTTP_403_FORBIDDEN,
        )
