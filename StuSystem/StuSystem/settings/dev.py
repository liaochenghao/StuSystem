from StuSystem.settings.common import *
# override common

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stu_system',
        'USER': 'root',
        'PASSWORD': '1q2w3e4r!Q',
        'HOST': '120.79.36.26',
        'PORT': 3306,
        # 'CHARSET': 'UTF-8',
        'OPTIONS': {'charset': 'utf8mb4'},
        'ATOMIC_REQUESTS': True
    }
}


REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/root/workspace/StuSystem/summer-web/dist'],
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

# mongodb配置
MONGODB_CONFIG = {
    'host': '42.51.8.152',
    'port': 50001,
    'user': 'stu_system',
    'password': 'qwe=-00.3690'
}

micro_service_domain = 'http://127.0.0.1:7071'
DOMAIN = 'http://shell.chinasummer.org'
BASE_MEDIA_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MEDIA_ROOT = '%s/media' % BASE_MEDIA_ROOT

MQ_SERVER = {
    'EXCHANGE': 'stu_system_exchange',
    'QUEUE_AUTO': 'stu_system_queue_auto',
    'QUEUE_NOTICE': 'stu_system_queue_notice',
    'URL_PARAMS': 'amqp://stu_system:qwe896275756@42.51.8.152:5672/stu_system'
}