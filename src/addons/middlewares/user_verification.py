from django.http import JsonResponse


class UserVerificationMiddleware:
    """
    Middleware for user verification.
    Ensures that authenticated users meet specific criteria
    (e.g., active status, not deleted, and valid role).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user

            # Verify if the user account is active
            if not user.is_active:
                return JsonResponse(
                    {"error": "Your account is inactive. Please contact support."},
                    status=403,
                )

            # Verify if the user account is marked as deleted
            # if user.is_deleted:
            #     return JsonResponse(
            #         {"error": "Not found."},
            #         status=404,
            #     )

            # Verify if the user has a valid role (optional)
            if user.role is None:
                return JsonResponse(
                    {
                        "error": "Your account role is not assigned. Please contact support."
                    },
                    status=403,
                )

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response


# from typing import Any, Type
#
# from django.contrib.auth import get_user_model
# from django.http import JsonResponse
# from django.http.request import HttpRequest
# from rest_framework import status
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.tokens import AccessToken
#
# UserModel = get_user_model()
# UserModelType = Type[UserModel]
#
#
# class UserVerificationMiddleware:
#     """
#     Middleware for verifying the status of user access based on the user status.
#
#     This middleware catches incoming requests and checks the validity of the user.
#     The user will be find by given JWT content in the `Authorization` request header.
#     If the user is deleted, returns a 403 Forbidden response, indicating that the user
#     has no permissions to perform the requested action.
#
#     If no user is found by given JWT, then it returns a 404 NotFound response.
#     Otherwise, it allows the request to proceed.
#     """
#
#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
#
#     def __call__(self, request: HttpRequest) -> JsonResponse | Any:
#         auth_header = request.headers.get("Authorization", "")
#         if auth_header:
#             try:
#                 token_obj = AccessToken(token=auth_header.split()[1])
#             except TokenError:
#                 return JsonResponse(
#                     data={"message": "Access token is invalid or expired. You can get another one."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#             user_id = token_obj.get("user_id")
#             user: UserModelType = UserModel.objects.only("deleted_at").filter(pk=user_id).first()
#             if user is None:
#                 return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#
#             if user.deleted_at is not None:
#                 return JsonResponse(
#                     data={"message": "You have no permissions to perform this action."}, status=status.HTTP_403_FORBIDDEN
#                 )
#
#         response = self.get_response(request)
#
#         return response
