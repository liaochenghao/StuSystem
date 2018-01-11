# coding: utf-8
from StuSystem.settings import micro_service_domain
from rest_framework import exceptions
import requests


class AuthorizeServer:
    """认证服务"""

    @staticmethod
    def ticket_authorize(ticket):
        url = "%s/api/stu_system/auth/authorize/" % micro_service_domain
        params = {'ticket': ticket}
        res = requests.get(url=url, params=params)
        if res.status_code != 200:
            raise exceptions.ValidationError('Micro Service 发生错误')
        if res.json()['code'] != 0:
            raise exceptions.ValidationError(res.json()['msg'])
        else:
            return res.json()['data']

    @staticmethod
    def create_ticket(user_id):
        url = "%s/api/stu_system/auth/authorize/" % micro_service_domain
        data = {'user_id': user_id}
        res = requests.post(url=url, data=data)
        if res.status_code != 200:
            raise exceptions.ValidationError('Micro Service 发生错误')

        if res.json()['code'] != 0:
            raise exceptions.ValidationError(res.json()['msg'])
        else:
            return res.json()['data']['ticket']

    @staticmethod
    def delete_ticket(ticket):
        url = "%s/api/stu_system/auth/authorize/" % micro_service_domain
        params = {'ticket': ticket}
        res = requests.get(url=url, params=params)
        if res.status_code != 200:
            raise exceptions.ValidationError('Micro Service 发生错误')
        else:
            if res.json()['code'] != 0:
                raise exceptions.ValidationError(res.json()['msg'])
            return res.json()['data']