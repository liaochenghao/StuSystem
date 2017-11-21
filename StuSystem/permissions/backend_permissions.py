# coding: utf-8
"""管理后台操作权限"""
from rest_framework import permissions


class BaseOperatePermission(permissions.BasePermission):
    """基础操作权限"""
    def has_permission(self, request, view):
        user = request.user
        if user.role == 'ADMIN':
            return True
        return False


class UserInfoOperatePermission(BaseOperatePermission):
    """用户信息操作权限"""


class OrderOperatePermission(BaseOperatePermission):
    """管理员订单操作权限"""
    pass


class CouponOperatePermission(BaseOperatePermission):
    """优惠券操作权限"""
    pass


class PaymentAccountInfoOperatePermission(BaseOperatePermission):
    """付款账号操作权限"""
    pass


class ChildUserOperatePermission(BaseOperatePermission):
    """子账号操作权限"""
    pass


class SalesManOperatePermission(BaseOperatePermission):
    """销售人员操作权限"""
    pass


class ProjectOperatePermission(BaseOperatePermission):
    """项目管理操作权限"""
    pass