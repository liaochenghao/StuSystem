# coding: utf-8
import pika
import time
import traceback
import logging
from EventAggregator.event_aggregator import EventAggregator
import threading
import json
from micro_service.stores.message_auto_notice import MessageAutoNotice
from StuSystem.settings import MQ_SERVER

log = logging.getLogger('tcp_server')
message_auto_notice = logging.getLogger('message_auto_notice')


class MqServer:
    def __init__(self):
        self._connection = None
        self._channel = None

    def __connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(MQ_SERVER['URL_PARAMS']))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(MQ_SERVER['EXCHANGE'], durable=True)

        self._channel.queue_declare(MQ_SERVER['QUEUE_AUTO'], durable=True)
        self._channel.queue_bind(queue=MQ_SERVER['QUEUE_AUTO'], exchange=MQ_SERVER['EXCHANGE'],
                                 routing_key='weixin_auto')
        self._channel.basic_consume(self._auto_message, MQ_SERVER['QUEUE_AUTO'], no_ack=True)

        self._channel.queue_declare(MQ_SERVER['QUEUE_NOTICE'], durable=True)
        self._channel.queue_bind(queue=MQ_SERVER['QUEUE_NOTICE'], exchange=MQ_SERVER['EXCHANGE'])

    def _auto_message(self, channel, basic_deliver, props, body):
        message = json.loads(body.decode('utf-8'))
        message_name = message.get('message_name', '')
        data = message['message_content']
        if message_name == 'message_auto_notice':
            message_auto_notice.info(message)
            EventAggregator().publish(MessageAutoNotice(**data))
        else:
            pass

    def dispose(self):
        if self._connection and self._connection.is_open:
            self._connection.close()

    def _start_consuming(self):
        try:
            self.__connect()
            print('MqServer 已启动...')
            self._channel.start_consuming()
        except Exception as err:
            self.dispose()
            print('发生错误, 2秒之后重连: %s' % format(err))
            log.error('发生错误, 2秒之后重连: %s' % traceback.format_exc())
            time.sleep(2)
            self.start()

    def start(self):
        threading.Thread(target=self._start_consuming, daemon=True).start()


MqServer = MqServer()