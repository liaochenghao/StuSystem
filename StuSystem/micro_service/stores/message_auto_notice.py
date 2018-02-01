# coding: utf-8


class MessageAutoNotice:
    """消息通知"""
    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.module_name = kwargs.pop('module_name')
        self.msg = kwargs.pop('msg')
        self.read = kwargs.pop('read', False)