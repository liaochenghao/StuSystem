from rest_framework import permissions


class AdminOperatePermission(permissions.BasePermission):
    """管理员操作权限"""
    def has_permission(self, request, view):
        user = request.user
        return True if user.role == 'ADMIN' else False