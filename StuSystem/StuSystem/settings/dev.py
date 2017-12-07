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

# mongodb配置
MONGODB_CONFIG = {
    'host': '42.51.8.152',
    'port': 50001,
    'user': 'stu_system',
    'password': 'qwe=-00.3690'
}

DOMAIN = 'http://42.51.8.152:8002'
MEDIA_ROOT = '/home/qiulei/workplace/StuSystem/media'