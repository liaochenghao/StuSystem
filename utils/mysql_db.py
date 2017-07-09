# coding: utf-8
import pymysql
from django.conf import settings

db_config = {
    'host': settings.DATABASES['default']['HOST'],
    'port': int(settings.DATABASES['default']['PORT']),
    'password': settings.DATABASES['default']['PASSWORD'],
    'db': settings.DATABASES['default']['NAME'],
    'user': settings.DATABASES['default']['USER']
}


def make_connection():
    return pymysql.connect(**db_config, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def execute_sql(sql):
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data