# coding: utf-8
from utils.single_ton import SingleTon


from urllib.parse import quote_plus

from pymongo import MongoClient

from StuSystem.settings import MONGODB_CONFIG


class Mongodb(metaclass=SingleTon):
    user = MONGODB_CONFIG.get('user')
    password = MONGODB_CONFIG.get('password')
    host = MONGODB_CONFIG.get('host')
    port = MONGODB_CONFIG.get('port')
    url = "mongodb://%s:%s@%s:%s/stu_system?authMechanism=SCRAM-SHA-1" % (quote_plus(user),
                                                                          quote_plus(password),
                                                                          quote_plus(host),
                                                                          port)

    def connection(self):
        mongodb = MongoClient(self.url)
        return mongodb

    @property
    def stu_system(self):
        """返回stu_system db 实例"""
        return self.connection()['stu_system']