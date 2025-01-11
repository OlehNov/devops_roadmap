import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_403_FORBIDDEN

# from config.settings import RESTRICTED_AREA


class RestrictAccessMiddleware:
    """
    Middleware to restrict access for inactive, deleted, or anonymous users
    to dynamically configured resources.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Get the user from the request
        user = getattr(request, "user", None)

        # Check if the user is anonymous, inactive, or deleted
        if (
            not user
            or isinstance(user, AnonymousUser)
            or not user.is_active
            or getattr(user, "is_deleted", False)
        ):
            # Get restricted paths and views from settings
            restricted_area = getattr(settings, "RESTRICTED_AREA", None)

            if not restricted_area:
                raise ValueError("RESTRICTED_AREA must be set")

            restricted_paths = restricted_area.get("PATHS", [])
            restricted_url_patterns = restricted_area.get(
                "URL_PATTERNS",
                [re.compile(f"^{path}.*$").pattern for path in settings.RESTRICTED_AREA.get("PATHS")]
            )
            restricted_excluded_paths = restricted_area.get("EXCLUDED_PATHS", [])

            current_path = request.path

            # Check if the path or view is restricted
            response = self.__check_access(
                current_path=current_path,
                restricted_paths=restricted_paths,
                restricted_url_patterns=restricted_url_patterns,
                restricted_excluded_paths=restricted_excluded_paths
            )
            if response:
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()  # Force rendering
                return response

        # Pass the request to the next middleware/view
        return self.get_response(request)

    def __check_access(self, current_path, **kwargs):
        if current_path in kwargs.get("restricted_paths"):
            return self._get_restricted_response()

        for pattern in kwargs.get("restricted_url_patterns"):
            if re.match(pattern, current_path) and current_path not in kwargs.get("restricted_excluded_paths"):
                return self._get_restricted_response()

    def _get_restricted_response(self):
        return Response(
            {
                "error": "Access denied. Your account is inactive, deleted, or you are not logged in."
            },
            status=HTTP_403_FORBIDDEN,
        )
