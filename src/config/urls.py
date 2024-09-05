from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('user/', include('tourists.urls')),
    path('glamp/', include('glamp.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path(
        'swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger',
    ),
]
