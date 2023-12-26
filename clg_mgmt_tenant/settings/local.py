from .base import * # noqa

ALLOWED_HOSTS = ['localhost']

DEBUG = os.environ.get('DEBUG', True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': 'db',
        'PORT': '5432',
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SIGNING_KEY": open(os.environ.get('JWT_PRIVATE_KEY','')).read(),
    "VERIFYING_KEY": open(os.environ.get('JWT_PUBLIC_KEY','')).read(),
}

CORS_ALLOW_ALL_ORIGINS = True