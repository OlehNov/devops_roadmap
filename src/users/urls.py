from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from users.views import (
    UserViewSet,
    ActivateUserAPIView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)


router = DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    path(
        "activate-user/<str:uuid64>/<str:token>/",
        ActivateUserAPIView.as_view(),
        name="activate-user",
    ),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
] + router.urls
