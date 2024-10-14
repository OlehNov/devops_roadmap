import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def handle_error(e):
    error_type = type(e).__name__

    if settings.DEBUG:
        response_data = {"error": f"{error_type}.", "traceback": traceback.format_exc()}
    else:
        response_data = {"error": f"{error_type}."}

    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


def validate_phone_error(e):
    if settings.DEBUG:
        return Response({"phone": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {
                "phone": "Validation error. Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


def validate_birthday_error(e):
    if settings.DEBUG:
        return Response({"birthday": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {
                "birthday": "Validation error. The date should be specified in the format YYYY-MM-DD."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
