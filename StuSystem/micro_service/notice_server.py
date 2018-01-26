# coding: utf-8
import json

import pika
from StuSystem.settings import MQ_SERVER


class NoticeServer:
    def __init__(self, **kwargs):
        # 根据不同需求传入mq配置, 默认为settings中系统配置
        self.url_params = kwargs.get('URL_PARAMS') if kwargs else MQ_SERVER['URL_PARAMS']
        self.exchange = kwargs.get('EXCHANGE') if kwargs else MQ_SERVER['EXCHANGE']
        self.queue_auto = kwargs.get('QUEUE_AUTO') if kwargs else MQ_SERVER['QUEUE_AUTO']
        self.queue_notice = kwargs.get('QUEUE_NOTICE') if kwargs else MQ_SERVER['QUEUE_NOTICE']

        self.connection = pika.BlockingConnection(pika.URLParameters(self.url_params))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange, durable=True)
        self.channel.queue_declare(self.queue_auto, durable=True)
        self.channel.queue_bind(queue=self.queue_auto, exchange=self.exchange)

    def close(self):
        self.connection.close()

    def publish(self, data):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue_auto,
                                   body=json.dumps(data))
        return


notice_server = NoticeServer()

# data = {
#     'message_name': 'message_auto_notice',
#     'message_content': {
#         'user_id': 2,
#         'module_name': 'order',
#         'read': False,
#         'msg': '您有一个新订单消息'
#     }
# }
# print('starting publish')
# while True:
#     notice_server.publish(data)
#     import time
#     time.sleep(2)
#     print('publish ok')