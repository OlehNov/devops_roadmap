from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from config.api import PingPongAPIView


ROOT_API = settings.ROOT_API


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PingPongAPIView.as_view(), name='ping'),
    path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger',
    ),
    path(
        f'{ROOT_API}/auth/',
        include(
            ('authentication.urls', 'authentication'),
            namespace='authentication',
        ),
    ),
    path(
        f'{ROOT_API}/tourists/',
        include(('tourists.urls', 'tourists'), namespace='tourists'),
    ),
    path(
        f'{ROOT_API}/users/',
        include(('users.urls', 'users'), namespace='users'),
    ),
    path(
        f'{ROOT_API}/glamps/',
        include(('glamps.urls', 'glamps'), namespace='glamps'),
    ),
    path(
        f'{ROOT_API}/eventlogs/',
        include(('eventlogs.urls', 'eventlogs'), namespace='eventlogs'),
    ),

]
