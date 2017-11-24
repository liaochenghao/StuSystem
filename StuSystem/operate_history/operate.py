# coding: utf-8
"""订单操作日志"""
from operate_history.models import OperateHistory


class BaseOperateHistoryHandle:
    """基础日志操作类"""

    def __init__(self, **kwargs):
        self.operate_method = dict(OperateHistory.OPERATE_KEY)
        self.source = kwargs.get('source')
        self.operator = kwargs.get('operator')
        self.key = kwargs.get('key', 'CREATE')
        self.remark = kwargs.get('remark')

    def create(self):
        """创建日志记录"""
        pass

    def read(self):
        """读取日志记录"""