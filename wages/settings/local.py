from .base import *
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.join(BASE_DIR, '../provision/local', '.env'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
