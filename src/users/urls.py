from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import UserTouristRegisterView, index, ActivateUserAPIView, PasswordResetRequestView, PasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path("", index, name="index"),
    path('tourist_reg/', UserTouristRegisterView.as_view(), name='tourist_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('activate-user/<str:uuid64>/<str:token>/', ActivateUserAPIView.as_view(), name="activate-user"),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('user_url/', include('config.urls')),
    # path('signup/', views.mail_notification),
]
