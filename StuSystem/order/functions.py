# coding: utf-8
from utils.future_help import run_on_executor
from EventAggregator.event_aggregator import EventAggregator
from micro_service.stores.message_auto_notice import MessageAutoNotice


@run_on_executor
def order_auto_notice_message(order, user):
    data = {
        'user_id': user.id,
        'module_name': 'order',
        'msg': '您有一条订单待支付，订单号为:%d' % order.id
    }
    EventAggregator.publish(MessageAutoNotice(**data))