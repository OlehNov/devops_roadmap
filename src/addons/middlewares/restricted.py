import re

from functools import partial

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.status import HTTP_403_FORBIDDEN

from addons.handlers.get_user_handler import aget_cached_user, get_cached_user
from addons.mixins.middleware_mixin import MiddlewareMixin


class RestrictAccessMiddleware(MiddlewareMixin):
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
        request.user = SimpleLazyObject(lambda: get_cached_user(request))
        request.auser = partial(aget_cached_user, request)

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
