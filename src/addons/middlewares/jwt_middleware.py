import jwt
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from addons.mixins.middleware_mixin import MiddlewareMixin

from config.settings import SECRET_KEY, ALGORITHM


class JWTDecoderMiddleware(MiddlewareMixin):
    """
    Middleware to check JWT token in the request header, decode it and add the user data to the request object.
    """
    def __call__(self, request):

        # Get header
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        if auth_header.startswith("Bearer "):
            # get token
            token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

                request.user_data = {
                    "token": token,
                    "token_type": decoded_token.get("token_type"),
                    "user_id": decoded_token.get("user_id"),
                    "email": decoded_token.get("email"),
                }
                request.user = self.get_user_from_token(decoded_token)

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)

        else:
            # Set anonymous user
            request.user_data = {
                "token": None,
                "token_type": "Anonymous",
                "user_id": None,
                "email": None,
            }
            request.user = AnonymousUser()


        return self.get_response(request)


    def get_user_from_token(self, decoded_token):
        """
        Retrieve the user object from the database using token data or set AnonymousUser.
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user_id = decoded_token.get("user_id")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
