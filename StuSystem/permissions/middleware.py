# -*- coding: utf-8 -*-
import json
from re import compile

import time
from django.conf import settings
from django.http.response import HttpResponse

from StuSystem.settings import mongodb
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
        if path.split('/')[1] == 'order' and request.user.role != 'STUDENT':
            return HttpResponse(content=json.dumps(dict(code=403, msg='您没有执行该操作的权限')),
                                content_type='application/json')


class AccessRecordMiddleWare(MiddlewareMixin):
    """接口访问记录"""
    def process_request(self, request):

        meta = request.META
        http_method = request.method
        get_data = request.GET
        body_data = json.loads(request.body) if request.body else None
        ticket = request.COOKIES.get('ticket')
        request_user_agent = meta.get('HTTP_USER_AGENT')
        url = request.path_info.lstrip('')
        self.data = {
            'url': url,
            'method': http_method,
            'user_agent': request_user_agent,
            'request_data': body_data if body_data else get_data,
            'ticket': ticket,
            'time': int(time.time()),
            'remote_addr': meta.get('REMOTE_ADDR'),
            'user_id': request.user.id
        }

    def process_response(self, request, response):
        stu_system = mongodb['stu_system']
        data = self.data
        data.update({
            'status_code': response.status_code,
            'response_data': response.data,
            'process_time': int(time.time()) - data.get('time')})
        stu_system.access_records.insert(data)
        return response