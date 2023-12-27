from .base import *  # noqa

ALLOWED_HOSTS = ["*"]

DEBUG = os.environ.get("DEBUG", True)  # noqa F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", ""),  # noqa F405
        "USER": os.environ.get("POSTGRES_USER", ""),  # noqa F405
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),  # noqa F405
        "HOST": "db",
        "PORT": "5432",
    }
}


SIMPLE_JWT.update( # noqa F405
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=15),  # noqa F405
        "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # noqa F405
        "SIGNING_KEY": open(os.environ.get("JWT_PRIVATE_KEY", "")).read(),  # noqa F405
        "VERIFYING_KEY": open(os.environ.get("JWT_PUBLIC_KEY", "")).read(),  # noqa F405
    }
)

CORS_ALLOW_ALL_ORIGINS = True
