"""
Django settings for yj project.

For more information on this file, see
https://docs.djangoproject.com/en//topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en//ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en//howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'syu*k+qn_u59$&jw9)!i_=l_+6a+lx_6h5sx&nh6pc_h$5ipus'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['yellowjackal.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yj',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yj.urls'

WSGI_APPLICATION = 'yj.wsgi.application'


# Database
# https://docs.djangoproject.com/en//ref/settings/#databases

DATABASES = {
    'dev_default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'd149bqjp4l9gq4',
      'USER': 'acmwffvfelomxx',
      'PASSWORD': 'ed527273b68ede2f591975569db689453c1888612f9429b8f51ac8e3cdb4df6c',
      'HOST': 'ec2-23-23-248-247.compute-1.amazonaws.com',
      'PORT': '5432',
      'URI': 'postgres://acmwffvfelomxx:ed527273b68ede2f591975569db689453c1888612f9429b8f51ac8e3cdb4df6c@ec2-23-23-248-247.compute-1.amazonaws.com:5432/d149bqjp4l9gq4'
    }
}

# Internationalization
# https://docs.djangoproject.com/en//topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en//howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(
        os.path.dirname(__file__),
        'static',
    ),
)
