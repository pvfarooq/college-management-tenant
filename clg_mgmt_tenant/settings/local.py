from .base import *  # noqa

ALLOWED_HOSTS = ["*"]

DEBUG = os.environ.get("DEBUG", True)  # noqa F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", ""),  # noqa F405
        "USER": os.environ.get("POSTGRES_USER", ""),  # noqa F405
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),  # noqa F405
        "HOST": os.environ.get("POSTGRES_HOST", ""),  # noqa F405
        "PORT": os.environ.get("POSTGRES_PORT", ""),  # noqa F405
    }
}

JWT_PRIVATE_KEY_PATH = os.environ.get("JWT_PRIVATE_KEY", "")  # noqa F405
JWT_PUBLIC_KEY_PATH = os.environ.get("JWT_PUBLIC_KEY", "")  # noqa F405
SIGNING_KEY = open(JWT_PRIVATE_KEY_PATH).read() if JWT_PRIVATE_KEY_PATH else ""
VERIFYING_KEY = open(JWT_PUBLIC_KEY_PATH).read() if JWT_PUBLIC_KEY_PATH else ""

SIMPLE_JWT.update(  # noqa F405
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=15),  # noqa F405
        "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # noqa F405
        "SIGNING_KEY": SIGNING_KEY,
        "VERIFYING_KEY": VERIFYING_KEY,
    }
)

CORS_ALLOW_ALL_ORIGINS = True
