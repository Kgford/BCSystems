import os
#import django_heroku
import pyodbc

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(SETTINGS_PATH,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(BASE_DIR,'media')
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/ipp/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index' 





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '+59a%cvpj6rm!=1a3=m40x@l6j7y3a-vl$%ykr6ynb86jj=&it'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['192.168.1.29','192.168.1.57','127.0.0.1','*']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'users',
    'inventory',
    'test',
    'stock',
    'shipping',
    'qa',
    'sales',
    'manufacturing',
    'planning',
    'E2',
    'process',
    'barcode_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]

ROOT_URLCONF = 'ipp.urls'

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

WSGI_APPLICATION = 'ipp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },

        'E2': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'IPPMFGSQL',
            'USER': 'sa',
            'PASSWORD': 'Secure1!',
            'HOST': 'IPP-E2',
            'PORT': '',
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',
                'unicode_results': True,
            }
        },   
        
        'TEST': {
                'ENGINE': 'sql_server.pyodbc',
                'NAME': 'ATE',
                'USER': 'developer',
                'PASSWORD': 'secure',
                'HOST': 'INN-SQLEXPRESS\SQLEXPRESS',
                'PORT': '',
                'OPTIONS': {
                    'driver': 'SQL Server Native Client 11.0',
                    'unicode_results': True,
                }               
            },
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


import dj_database_url 
DATABASE_CONNECTION_POOLING = False
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
#django_heroku.settings(locals())
SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
SESSION_TIMEOUT_REDIRECT = 'index'