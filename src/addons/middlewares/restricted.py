from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.urls import resolve
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_403_FORBIDDEN


class RestrictInactiveOrDeletedUserMiddleware:
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
            restricted_views = getattr(settings, "RESTRICTED_VIEWS", [])
            restricted_url_patterns = getattr(settings, "RESTRICTED_URL_PATTERNS", [])

            current_path = request.path
            try:
                current_view = resolve(request.path).view_name
            except Exception:
                current_view = None

            # Check if the path or view is restricted
            if current_path in (restricted_paths or restricted_url_patterns) or (
                current_view and current_view in restricted_views
            ):
                response = Response(
                    {
                        "error": "Access denied. Your account is inactive, deleted, or you are not logged in."
                    },
                    status=HTTP_403_FORBIDDEN,
                )
                # Set renderer for the response
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()  # Force rendering
                return response

        # Pass the request to the next middleware/view
        return self.get_response(request)
