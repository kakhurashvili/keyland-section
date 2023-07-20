
from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import random
import string

# Generate a random secret key
def generate_secret_key():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(50))

# Get or generate the secret key
SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secret_key()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['www.keyland.ge', 'keyland.ge']


# Application definition

INSTALLED_APPS = [
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admindashboard',
    'storeapp',
    'core',
    'UserProfile',
    'api',
    'colorfield',
    #'sslserver',

    'ckeditor',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'UserProfile.middleware.EarningPointsMiddleware',


]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'storeapp.context_processors.cart_renderer',
                'storeapp.context_processors.main_category',
                'storeapp.context_processors.saved_item',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# Database
#https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

# """ DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ecom',
#         'USER': 'postgres',
#         'PASSWORD': 'database',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# } """



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ecommerce',
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#         'HOST':  os.environ.get('DB_HOST'),
#         'PORT': '5432'
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tbilisi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'admindashboard', 'static'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# HTTPS/SSL Configuration
# Replace the placeholders with the appropriate paths and settings for your environment

# Set secure proxy headers if your Django application is behind a reverse proxy like Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Set the secure cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Session timeout set to 30 days (in seconds)
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60

# # Set HSTS (HTTP Strict Transport Security) headers
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Set the SSL/TLS certificate file paths
# Replace '/path/to/ssl_certificate.crt' with the actual path to your SSL/TLS certificate file
# Replace '/path/to/ssl_certificate.key' with the actual path to your SSL/TLS private key file
# If using Let's Encrypt, you can specify the certificate and key file paths provided by Let's Encrypt
# You can also use Certbot or another ACME client to automate the certificate management
# SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = 443
SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True


# # SSL certificate and key file paths
# CERT_FILE = os.path.join(BASE_DIR, 'cert.pem')
# KEY_FILE = os.path.join(BASE_DIR,  'key.pem')

# # Use the file paths in your Django settings
# SSLCERTFILE = CERT_FILE
# SSLKEYFILE = KEY_FILE
# # Set the SSL certificate and key file paths


# # Optional: Set the SSL server port (default is 8443)
# SSLPORT = 8443

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = 'account'



CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 900,
    },
}

GEOIP_PATH = os.path.join( 'geoip')

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')
# INSTAGRAM_ACCESS_TOKEN = '659827719341889'

# INSTAGRAM_CLIENT_SECRET = '573285304824c67565ec6e3bbfa44c86'

# AWS_QUERYSTRING_AUTH = False
# AWS_S3_FILE_OVERWRITE = False
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID  = os.environ.get('AWS_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY =  os.environ.get('AWS_SECRET_KEY')
# AWS_STORAGE_BUCKET_NAME = 'shopit-bucket'