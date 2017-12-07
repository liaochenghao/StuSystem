# coding: utf-8
from utils.single_ton import SingleTon


from urllib.parse import quote_plus

from pymongo import MongoClient

from StuSystem.settings import MONGODB_CONFIG


class Mongodb(metaclass=SingleTon):

    def __int__(self):
        self._user = MONGODB_CONFIG.get('user')
        self._password = MONGODB_CONFIG.get('password')
        self._host = MONGODB_CONFIG.get('host')
        self._port = MONGODB_CONFIG.get('port')
        self._url = "mongodb://%s:%s@%s:%s/stu_system?authMechanism=SCRAM-SHA-1" % (quote_plus(self._user),
                                                                                    quote_plus(self._password),
                                                                                    quote_plus(self._host),
                                                                                    self._port)

    def __connection(self):
        mongodb = MongoClient(self._url)
        return mongodb

    def stu_system(self):
        """返回stu_system db 实例"""
        return self.__connection()['stu_system']