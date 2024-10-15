import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-k$83@$)75u_^s==b+!rf%3^99-mrw7-0o43)yw0@tb8i8^acil"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "celery",
    "cloudinary",
    "cloudinary_storage",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",

    "administrators",
    "authentication",
    "categories",
    "eventlogs",
    "glamps",
    "roles",
    "tourists",
    "users",
]

AUTH_USER_MODEL = "users.User"

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_API = "api/v1"

ROOT_URLCONF = "config.urls"

CORS_ALLOW_ALL_ORIGINS = True

# Templates Settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.mysql"),
        "NAME": os.getenv("DB_NAME", default="glamp"),
        "USER": os.getenv("DB_USER", default="glamp_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", default="glamp_password"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": int(os.getenv("DB_PORT", default="3306")),
    },
    "eventlog": {
        "ENGINE": os.getenv("EVENTLOGS_DB_ENGINE", default="django.db.backends.mysql"),
        "NAME": os.getenv("EVENTLOGS_DB_NAME", default="eventlog"),
        "USER": os.getenv("EVENTLOGS_DB_USER", default="glamp_user"),
        "PASSWORD": os.getenv("EVENTLOGS_DB_PASSWORD", default="glamp_password"),
        "HOST": os.getenv("EVENTLOGS_DB_HOST", default="localhost"),
        "PORT": int(os.getenv("EVENTLOGS_DB_PORT", default="3306")),
    },
}


# REST FRAMEWORK Settings
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# Simple JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "users.validators.NoSpacePasswordValidator",
    },
    {
        "NAME": "users.validators.LatinOnlyPasswordValidator",
    },
    {
        "NAME": "users.validators.DigitRequiredPasswordValidator",
    },
    {
        "NAME": "users.validators.UpperLowerCasePasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
VIDEO_URL = "/video/"


# Cloudinary storage settings

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = os.getenv("CLOUDINARY_DEFAULT_FILE_STORAGE")
STATICFILES_STORAGE = os.getenv("CLOUDINARY_STATICFILES_STORAGE")
DEFAULT_VIDEO_STORAGE = os.getenv("CLOUDINARY_DEFAULT_VIDEO_STORAGE")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Spectacular Settings
SPECTACULAR_SETTINGS = {
    "TITLE": "GLAMP API",
    "DESCRIPTION": "GLAMP REST API.",
    "VERSION": "1.0.0",
    # 'TOS': 'https://example.com/terms/',
    "CONTACT": {
        "name": "API Support",
        # 'url': 'https://example.com/support/',
        "email": "born2code.py@gmail.com",
    },
    # 'LICENSE': {
    #     'name': 'MIT License',
    #     'url': 'https://opensource.org/licenses/MIT',
    # },
    # 'SCHEMA_PATH_PREFIX': '/api/',  # To exclude common path prefixes like '/api/' from the schema
    "SERVE_INCLUDE_SCHEMA": False,  # Whether to include schema in Swagger UI responses or not
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.AllowAny"
    ],  # Permissions for serving schema
    "COMPONENT_SPLIT_REQUEST": True,  # Split request and response components
    # 'POSTPROCESSING_HOOKS': [],  # A list of functions to customize the schema generation process
    # 'ENUM_NAME_OVERRIDES': {},  # Mapping for overriding enum names
    "SORT_OPERATION_PARAMETERS": True,  # Sort parameters in operations
    "SCHEMA_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    # 'AUTHENTICATION_WHITELIST': [],  # Authentication classes that should always be included in security definitions
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelsExpandDepth": 1,
    },
    "REDOC_UI_SETTINGS": {
        "hideDownloadButton": True,
        "pathInMiddlePanel": True,
        "theme": {
            "spacing": {
                "unit": 10,
                "sectionHorizontal": 20,
            },
        },
    },
    "PREPROCESSING_HOOKS": [],  # Pre-processing hooks to modify or inspect the schema
}


# JazzMin Settings

JAZZMIN_SETTINGS = {
    "site_title": "Glamp",
    "site_header": "Glamp",
    "site_brand": "Glamp Administration",
    "welcome_sign": "Glamp Admin Panel",
    "search_model": [],
    "topmenu_links": [{"app": "glamps"}],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_models": [
        "auth.group",
        "sites.site",
    ],
    "order_with_respect_to": [
        "users",
        "profiles",
    ],
    "icons": {
        "glamps.glamp": "fas fa-campground",
    },
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
    "related_modal_active": False,
}


# CELERY Settings
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", default="redis://broker:6379/0")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", default="redis://broker:6379/0"
)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# Cache Settings

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.getenv('CELERY_LOCATION'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

try:
    from .settings_local import *
except ImportError:
    pass

if DEBUG:
    REST_FRAMEWORK = {
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend"
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            # 'rest_framework.authentication.SessionAuthentication',
            "rest_framework.authentication.BasicAuthentication",
        ],
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ],
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
    }
