import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_403_FORBIDDEN


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
            restricted_paths = getattr(settings, "RESTRICTED_PATHS", [])
            restricted_url_patterns = getattr(settings, "RESTRICTED_URL_PATTERNS", [])

            current_path = request.path

            # Check if the path or view is restricted
            response = self.__check_access(current_path, restricted_paths, restricted_url_patterns)
            if response:
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()  # Force rendering
                return response

        # Pass the request to the next middleware/view
        return self.get_response(request)

    def __check_access(self, current_path, restricted_paths, restricted_url_patterns):
        if current_path in restricted_paths:
            return self._get_restricted_response()

        for pattern in restricted_url_patterns:
            if re.match(pattern, current_path):
                return self._get_restricted_response()

    def _get_restricted_response(self):
        return Response(
            {
                "error": "Access denied. Your account is inactive, deleted, or you are not logged in."
            },
            status=HTTP_403_FORBIDDEN,
        )
