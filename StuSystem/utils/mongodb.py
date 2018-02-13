# coding: utf-8
import time

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

    def find(self, collection_name, search_data, pagination=False, db_name='stu_system',
             page_size=10, page=1, sort_field=None):
        """
        :param collection_name: 集合名称
        :param search_data:     筛选条件
        :param pagination:      是否需要分页，默认为False
        :param sort_field:      排序方式，默认以_id正向排序
        :param db_name:         数据库名称，默认为stu_system
        :param page_size:       每页数据条数，默认为10条
        :param page:            当前页数，默认为1
        :return:
        """
        if not sort_field:
            sort_field = ("_id", 1)
        db = self.connection()[db_name]
        if pagination:
            return db.get_collection(collection_name).find(search_data).skip(page-1).limit(page_size).sort([sort_field])
        else:
            return db.get_collection(collection_name).find(search_data).sort([sort_field])

    def insert(self, collection_name, insert_data, db_name='stu_system'):
        """
        :param collection_name:   集合名称
        :param insert_data:       插入数据
        :param db_name:           数据库名称，默认为stu_system
        :return:
        """
        insert_data['create_time'] = int(time.time())
        db = self.connection()[db_name]
        return db.get_collection(collection_name).insert(insert_data)

    def update_one(self, collection_name, search_data, update_data, db_name='stu_system'):
        """
        :param collection_name:    集合名称
        :param search_data:        筛选条件
        :param update_data:        更新的数据
        :param db_name:            数据库名称，默认为stu_system
        :return:
        """
        db = self.connection()[db_name]
        return db.get_collection(collection_name).update(search_data, update_data)

    def update_many(self, collection_name, search_data, update_data, db_name='stu_system'):
        """
        :param collection_name:    集合名称
        :param search_data:        筛选条件
        :param update_data:        更新的数据
        :param db_name:            数据库名称，默认为stu_system
        :return:
                """
        db = self.connection()[db_name]
        return db.get_collection(collection_name).update(search_data, update_data, multi=True)


stu_db = Mongodb()

