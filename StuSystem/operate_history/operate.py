# coding: utf-8
"""订单操作日志"""
from rest_framework import exceptions
from operate_history.models import OperateHistory, OrderOperateHistory
from operate_history.serializers import OrderOperateHistorySerializer

operate_method = dict(OperateHistory.OPERATE_KEY)


class BaseOperateHistoryHandle:
    """基础日志操作类"""

    def __init__(self, **kwargs):
        self.source = kwargs.get('source')
        self.operator = kwargs.get('operator')
        self.key = kwargs.get('key', 'CREATE')
        self.remark = kwargs.get('remark')
        self.source_type = kwargs.get('source_type')

    def __validate(self):
        if self.operator or self.remark is None:
            raise BaseException('operator, remark不能为空')

    def create_record(self):
        """创建日志记录"""
        pass

    def read_records(self):
        """读取日志记录"""
        pass

    def find_records_by_operator(self):
        """根据操作者查询操作记录"""
        pass


class HistoryType:
    """日志类型"""
    @staticmethod
    def history_type(kwargs):
        if kwargs.get('source_type') == 'ORDER':
            return OrderOperateHistory
        else:
            raise exceptions.ParseError('请传入正确的资源类型')


class OperateHistoryHandle(BaseOperateHistoryHandle):
    """日志操作类"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = HistoryType.history_type(kwargs)

    def create_record(self):
        self.model.objects.create(operator=self.operator, key=self.key, source=self.source, remark=self.remark)
        return

    def read_records(self):
        sources = self.model.objects.filter(source=self.source)
        records = OrderOperateHistorySerializer(sources, many=True).data
        return records

    def find_records_by_operator(self):
        sources = self.model.objects.filter(operator=self.operator)
        records = OrderOperateHistorySerializer(sources, many=True).data
        return records


