"""
Django settings for StuSystem project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2&x74*2^ffs6coogjrh-@7n#!c5dgd@vhw^h+)8tw(_7orzlmk'

ROOT_URLCONF = 'StuSystem.urls'

WSGI_APPLICATION = 'StuSystem.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../../../static'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]

DOMAIN = 'http://apply.chinasummer.org'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')

if not os.path.isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '42.51.8.152']

# 不需要校验权限, 免登陆
LOGIN_EXEMPT_URLS = [
    r'auth/user/login',
    r'auth/user/check_account',
    r'auth/user/assign_sales_man',
    r'auth/user/authorize',
    r'^$',
]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'debug_toolbar',
    'admin',
    'authentication',
	'corsheaders',
    'common',
    'source',
    'coupon',
    'market',
    'order',
    'gunicorn',
    'operate_history'
]


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'permissions.middleware.AuthorizeRequiredMiddleWare',
    'permissions.middleware.AccessRecordMiddleWare',
    'permissions.middleware.BackendAPIRequestMiddleWare'
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = '^.*$'
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ('Content-Type', 'X-Requested-With',)

# https://docs.djangoproject.com/en/1.11/ref/settings/#databasesREST_FRAMEWORK = {
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend', 'rest_framework.filters.SearchFilter'),
    'DEFAULT_RENDERER_CLASSES': (
        'utils.renderers.CustomJsonRender',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'utils.Auth.SessionCsrfExemptAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'utils.handlers.exception_handler'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LOG_ROOT = os.path.join(BASE_DIR, '../../logs')

if not os.path.isdir(LOG_ROOT):
    os.makedirs(LOG_ROOT)


# 日志系统
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        }
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/error.log' % LOG_ROOT,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

# 微信服务号配置
WX_CONFIG = {
    'APP_ID': 'wx6cdbbafe0da85703',
    'APP_SECRET': '73c8e307c09027162840705e7496ed32'
}

WX_SMART_PROGRAM = {
    'APP_ID': 'wxf2b2b9c7133fe56f',
    'APP_SECRET': '13a268b3ffb689a7d6c38245cc7ded2f'
}

LANGUAGE_CODE = 'zh-cn'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True