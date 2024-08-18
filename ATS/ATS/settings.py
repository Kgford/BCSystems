import os
import django_heroku
import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(SETTINGS_PATH,'templates')
MEDIA_DIR = os.path.join(BASE_DIR,'media')
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = 'staff/user_login'
LOGIN_REDIRECT_URL = 'staff/user_login'
LOGOUT_REDIRECT_URL = 'staff/user_login' 
AUTH_PROFILE_MODULE = 'users.UserProfileInfo'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails') 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_USER = EMAIL_HOST_USER.replace("'", "")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD.replace("'", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
CLOUDINARY_STORAGE = {
             'CLOUD_NAME': 'automated-test-solutions',
             'API_KEY': '744644621367363',
             'API_SECRET': os.environ.get('API_SECRET')
            }

DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_URL='cloudinary://744644621367363:' + os.environ.get('API_SECRET') + '@automated-test-solutions'

#~~~~~~~~~~~~~~~~~~~~~~~~STATICFILES_STORAGE~~Django~~~~~~~~~~~~~~~~~~~~~~~~~~~
#STATIC_DIR = os.path.join(BASE_DIR,'static')
#STATICFILES_DIRS = [STATIC_DIR]
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
#STATIC_URL = '/static/'
#~~~~~~~~~~~~~~~~~~~~~~~~STATICFILES_STORAGE~~Django~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~STATICFILES_STORAGE~~WhiteNoiseMiddleware~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Whitenoise Storage Class  - Apply compression but don’t want the caching behaviour
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#~~~~~~~~~~~~~~~~~~~~~~~~STATICFILES_STORAGE~~WhiteNoiseMiddleware~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
TILL_USERNAME = os.environ.get('TILL_USERNAME')
TILL_API_KEY = os.environ.get('TILL_API_KEY')


ALLOWED_HOSTS = ['www.automatedtestsolutions.com','automatedtestsolutions.com','automatedtestsolution.com','automatedtestsolutions.herokuapp.com','127.0.0.1', 'localhost']



# Application definition

INSTALLED_APPS = [
    'users',
    'equipment',
    'client',
    'contractors',
    'dashboard',
    'locations',
    'inventory',
    'atspublic',
    'accounts',
    'assets',
    'vendor',
    'phone_field',
    'user_visit',
    'barcode_app',
    'whitenoise.runserver_nostatic',
    'cloudinary',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'ATS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'ATS.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'd1425g59gt7psr',

        'USER': 'ufv2lnanens5ld',

        'PASSWORD': 'p519ca7d03c3317226cd85c069742cb2ccd1ebc2bc2212175176db05a60d9518e',

        'HOST': 'ec2-52-205-207-244.compute-1.amazonaws.com',

        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
SESSION_TIMEOUT_REDIRECT = 'staff/user_login'
