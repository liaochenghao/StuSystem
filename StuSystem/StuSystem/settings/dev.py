from StuSystem.settings.common import *

# override common

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stu_system',
        'USER': 'root',
        'PASSWORD': 'qwe896275756',
        'HOST': '42.51.8.152',
        'PORT': 3306,
        'CHARSET': 'UTF-8',
        'ATOMIC_REQUESTS': True
    }
}