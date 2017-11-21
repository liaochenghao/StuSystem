# -*- coding: utf-8 -*-
import json
from re import compile

from django.conf import settings
from django.http.response import HttpResponse

from authentication.functions import UserTicket

EXEMPT_URLS = []
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class AuthorizeRequiredMiddleWare(MiddlewareMixin):
    """用户认证中间件"""
    def process_request(self, request):
        path = request.path_info.lstrip('/')
        for m in EXEMPT_URLS:
            if m.match(path):
                return

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            ticket = request.GET.get('ticket')
        if not ticket:
            return HttpResponse(content=json.dumps(dict(code=401, msg='未登陆')),
                                content_type='application/json')

        user = UserTicket.check_ticket(ticket)
        if not user:
            return HttpResponse(content=json.dumps(dict(code=401, msg='未登陆')),
                                content_type='application/json')
        request.user = user


class BackendAPIRequestMiddleWare(MiddlewareMixin):
    """管理后台接口访问限制中间件"""
    def process_request(self, request):
        path = request.path_info.lstrip('')
        if path.split('/')[1] == 'admin' and request.user.role == 'STUDENT':
            return HttpResponse(content=json.dumps(dict(code=403, msg='您没有执行该操作的权限')),
                                content_type='application/json')