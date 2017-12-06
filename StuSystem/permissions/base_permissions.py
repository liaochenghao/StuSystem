# coding: utf-8
"""管理后台操作权限"""
from authentication.models import User
from rest_framework import permissions


class BaseOperatePermission(permissions.BasePermission):
    """基础操作权限"""
    roles = User.ROLE
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def operate_permission(self, request, view):
        if request.user.role in ['ADMIN', 'MARKET', 'PRODUCT', 'FINANCE', 'SALES']:
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


class CreateCouponOperatePermission(BaseOperatePermission):
    """创建优惠券操作权限"""
    def operate_permission(self, request, view):
        if request.user.role in ['ADMIN', 'FINANCE']:
            return True
        else:
            return False


class UserCouponOperatePermission(BaseOperatePermission):
    """分配优惠券操作权限"""
    def operate_permission(self, request, view):
        if request.user.role in ['ADMIN', 'SALES']:
            return True
        else:
            return False


class StudentOperatePermission(BaseOperatePermission):
    """学生操作权限"""

    def operate_permission(self, request, view):
        if request.user.role == 'STUDENT':
            return True
        else:
            return False


class StudentReadOnlyPermission(BaseOperatePermission):
    """学生只读操作权限"""

    def operate_permission(self, request, view):
        if request.user.role == 'STUDENT':
            if request.method in self.SAFE_METHODS:
                return True
            else:
                return False
        else:
            return True


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


class SalesOperatePermission(BaseOperatePermission):
    """销售操作权限"""
    def operate_permission(self, request, view):
        if request.user.role == 'SALES':
            return True
        else:
            return False