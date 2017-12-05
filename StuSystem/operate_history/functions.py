# coding: utf-8

from operate_history.operate import OperateHistoryHandle


class HistoryFactory:
    @staticmethod
    def create_record(operator, source, source_type, key, remark):
        """创建日志记录"""
        operate_handle = OperateHistoryHandle(operator=operator, source=source, source_type=source_type, key=key,
                                              remark=remark)
        return operate_handle.create_record()

    @staticmethod
    def read_records(source_type, source):
        """读取记录"""
        operator_handle = OperateHistoryHandle(source=source, source_type=source_type)
        return operator_handle.read_records()