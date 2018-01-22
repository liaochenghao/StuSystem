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

    def find(self, collection_name, search_data, db_name='stu_system'):
        db = self.connection()[db_name]
        return db.get_collection(collection_name).find(search_data)

    def insert(self, collection_name, insert_data, db_name='stu_system'):
        db = self.connection()[db_name]
        return db.get_collection(collection_name).insert(insert_data)

    def update_one(self, collection_name, search_data, update_data, db_name='stu_system'):
        db = self.connection()[db_name]
        return db.get_collection(collection_name).update(search_data, update_data)

    def update_many(self, collection_name, search_data, update_data, db_name='stu_system'):
        db = self.connection()[db_name]
        return db.get_collection(collection_name).update(search_data, update_data, multi=True)


stu_db = Mongodb()

