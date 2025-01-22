from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import (
    PasswordResetConfirmView,
    PasswordResetRequestView,
    UserViewSet
)

router = DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
] + router.urls
