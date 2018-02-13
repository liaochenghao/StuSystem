# coding: utf-8
import time
from EventAggregator.event_aggregator import EventAggregator
from micro_service.stores.message_auto_notice import MessageAutoNotice
from utils.mongodb import stu_db


def message_auto_notice(message_auto_notice: MessageAutoNotice):
    insert_data = {
        'module_name': message_auto_notice.module_name,
        'user_id': message_auto_notice.user_id,
        'read': message_auto_notice.read,
        'msg': message_auto_notice.msg,
        'create_time': int(time.time())
    }
    stu_db.insert(collection_name='message_auto_notice', insert_data=insert_data)


def subscribe():
    EventAggregator.subscribe(MessageAutoNotice, message_auto_notice)
