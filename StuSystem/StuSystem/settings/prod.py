from StuSystem.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '122.114.6.232', '47.92.115.126', 'apply.chinasummer.org']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/root/project/summer-web-h5-build'],
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

STATIC_ROOT = os.path.abspath('/root/project/summer-web-h5-build')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stu_system',
        'USER': 'root',
        'PASSWORD': 'svLE26eg',
        'HOST': '47.92.115.126',
        'PORT': 3306,
        'CHARSET': 'UTF-8',
        'ATOMIC_REQUESTS': True
    }
}