# coding: utf-8
from rest_framework import permissions


class OrderOperatePermission(permissions.BasePermission):
    """管理员订单操作权限"""
    def has_permission(self, request, view):
        user = request.user
        return True if user.role == 'ADMIN' else False


class CouponOperatePermission(permissions.BasePermission):
    """优惠券操作权限"""
    def has_permission(self, request, view):
        user = request.user
        if user.role == 'ADMIN':
            return True
        return False