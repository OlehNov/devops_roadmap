from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
import debug_toolbar

from config import api


ROOT_API = settings.ROOT_API


urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", api.ping_pong_view, name="ping"),
    path("api/schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        f"{ROOT_API}/auth/",
        include(
            ("authentication.urls", "authentication"),
            namespace="authentication",
        ),
    ),
    path(
        f"{ROOT_API}/glamp-owners/",
        include(
            ("glamp_owners.urls", "glamp-owners"),
            namespace="glamp-owners",
        ),
    ),
    path(
        f"{ROOT_API}/tourists/",
        include(("tourists.urls", "tourists"), namespace="tourists"),
    ),
    path(
        f"{ROOT_API}/administrators/",
        include(
            ("administrators.urls", "administrators"),
            namespace="administrators",
        ),
    ),
    path(
        f"{ROOT_API}/managers/",
        include(
            ("managers.urls", "managers"),
            namespace="managers",
        ),
    ),
    path(
        f"{ROOT_API}/users/",
        include(("users.urls", "users"), namespace="users"),
    ),
    path(
        f"{ROOT_API}/categories/",
        include(("categories.urls", "categories"), namespace="categories"),
    ),
    path(
        f"{ROOT_API}/glamps/",
        include(("glamps.urls", "glamps"), namespace="glamps"),
    ),
    path(
        f"{ROOT_API}/eventlogs/",
        include(("eventlogs.urls", "eventlogs"), namespace="eventlogs"),
    ),
]
