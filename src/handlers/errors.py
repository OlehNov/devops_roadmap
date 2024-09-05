import traceback
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def handle_error(e):
    error_type = type(e).__name__

    if settings.DEBUG:
        response_data = {
            "error": f"{error_type}.",
            "traceback": traceback.format_exc()
        }
    else:
        response_data = {
            "error": f"{error_type}."
        }

    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
