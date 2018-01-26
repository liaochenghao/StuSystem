# coding: utf-8
from micro_service.mq_server import MqServer


def start_auto_task():
    # 开启MqServer任务
    MqServer.start()