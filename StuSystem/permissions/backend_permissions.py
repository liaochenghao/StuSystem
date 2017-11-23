# coding: utf-8
"""管理后台操作权限"""
from authentication.models import User
from rest_framework import permissions


class BaseOperatePermission(permissions.BasePermission):
    """基础操作权限"""
    roles = User.ROLE

    def operate_permission(self, request, view):
        if request.user.role in ['ADMIN', 'MARKET', 'PRODUCT', 'FINANCE']:
            return True
        else:
            return False

    def has_permission(self, request, view):
        if self.operate_permission(request, view):
            return True
        return False


class AdminOperatePermission(BaseOperatePermission):
    """管理员操作权限"""
    def operate_permission(self, request, view):
        if request.user.role == 'ADMIN':
            return True
        else:
            return False


class StudentOperatePermission(BaseOperatePermission):
    """学生操作权限"""

    def operate_permission(self, request, view):
        return False


class MarketOperatePermission(BaseOperatePermission):
    """市场部操作权限"""

    def operate_permission(self, request, view):
        if request.user.role == 'MARKET':
            return True
        else:
            return False


class ProductOperatePermission(BaseOperatePermission):
    """产品部操作权限"""
    def operate_permission(self, request, view):
        if request.user.role == 'PRODUCT':
            return True
        else:
            return False


class FinanceOperatePermission(BaseOperatePermission):
    """财务部操作权限"""

    def operate_permission(self, request, view):
        if request.user.role == 'FINANCE':
            return True
        else:
            return False