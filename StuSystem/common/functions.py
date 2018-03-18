# coding: utf-8
import time
from EventAggregator.event_aggregator import EventAggregator
from micro_service.stores.message_auto_notice import MessageAutoNotice
from utils.mongodb import stu_db
import logging

logger = logging.getLogger('django')


def message_auto_notice(message_auto_notice: MessageAutoNotice):
    insert_data = {
        'module_name': message_auto_notice.module_name,
        'user_id': message_auto_notice.user_id,
        'read': message_auto_notice.read,
        'msg': message_auto_notice.msg,
        'create_time': int(time.time())
    }
    try:
        logger.info('message_auto_notice insert data start: %s' % insert_data)
        stu_db.insert_one(collection_name='message_auto_notice', insert_data=insert_data)
        logger.info('message_auto_notice insert data end: %s' % insert_data)
    except Exception as e:
        logger.info('Exception message_auto_notice exception e:')
        raise e


def subscribe():
    EventAggregator.subscribe(MessageAutoNotice, message_auto_notice)
