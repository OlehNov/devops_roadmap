from django.urls import path

from authentication.api import (
    CustomObtainTokenPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView, UserLogoutView,
)

urlpatterns = [
    path("token/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
