from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from src.config.api import PingView

urlpatterns = [
    path('ping', PingView.as_view(), name='ping'),
    path('admin/', admin.site.urls),
    path('users/tourists/', include('tourists.urls')),
    path('users/', include('users.urls')),
    path('glamps/', include('glamp.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger',
    ),
]
