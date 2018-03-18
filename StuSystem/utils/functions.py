# coding: utf-8
import time
import datetime
import logging

logger = logging.getLogger("django")


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
    logger.info('Deal with Mongodb Method(handle_mongodb_cursor_data) start : %s' % str(datetime.datetime.now()))
    try:
        logger.info('----------------------mongo_cursor:%s' % mongo_cursor)
        cursor_data = list(mongo_cursor)
        logger.info('----------------------cursor_data:%s' % cursor_data)
        for item in cursor_data:
            item['id'] = str(item.pop('_id'))
            if item.get('create_time'):
                item['create_time'] = timestamp_to_datetime(item.pop('create_time'))
    except Exception as e:
        logger.info('Mongodb Error: %s' % str(e))
        cursor_data = None
    logger.info('Deal with Mongodb Method(handle_mongodb_cursor_data) end : %s' % str(datetime.datetime.now()))
    return cursor_data
