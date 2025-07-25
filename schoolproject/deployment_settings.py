import os 
import dj_database_url
from schoolproject.settings import *
from schoolproject.settings import BASE_DIR

print("✅ deployment_settings.py is being used1")

ALLOWED_HOSTS = ['school-management-backend-ftec.onrender.com', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://school-management-backend-ftec.onrender.com']

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'schoolproject.middleware.AutoLoginMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://school-management-frontend-5x70.onrender.com'
]


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    }
}


DATABASES = {
    'default': dj_database_url.config(
        default = os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ),
}

