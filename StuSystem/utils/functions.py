# coding: utf-8
import time
import datetime


def get_key_verbose_data(data: dict):
    """将dict数据结构变为key,verbose的list"""
    res = []
    for key, value in data.items():
        res.append({'key': key, 'verbose': value}),
    return res


def timestamp_to_datetime(int_time: int):
    """将时间戳转换成utc时间的字符串"""
    struct_time = time.gmtime(int_time)
    tm_year = struct_time.tm_year
    tm_mon = struct_time.tm_mon
    tm_day = struct_time.tm_mday
    tm_hour = struct_time.tm_hour
    tm_min = struct_time.tm_min
    tm_sec = struct_time.tm_sec
    time_str = "%s-%s-%sT%s:%s:%sZ" % (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)
    return time_str


def handle_mongodb_cursor_data(mongo_cursor):
    """将mongodb查询出的cursor转换为list数据的data"""
    try:
        cursor_data = list(mongo_cursor)
        for item in cursor_data:
            item['id'] = str(item.pop('_id'))
            item['create_time'] = timestamp_to_datetime(item.pop('create_time'))
    except TypeError:
        cursor_data = None
    return cursor_data