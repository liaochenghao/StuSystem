# coding: utf-8
from StuSystem.settings import micro_service_domain
from rest_framework import exceptions
import requests


class BaseHttpServer:

    @staticmethod
    def get(url, params):
        try:
            res = requests.get(url=url, params=params)
        except:
            raise exceptions.ValidationError('微服务发生错误')
        if not res.status_code == 200:
            raise exceptions.ValidationError('微服务发生错误，返回非200类消息')
        if res.json()['code'] != 0:
            raise exceptions.ValidationError('验证错误: %s' % res.json()['msg'])
        return res.json()['data']

    @staticmethod
    def post(url, json_data):
        try:
            res = requests.post(url=url, json=json_data)
        except:
            raise exceptions.ValidationError('微服务发生错误')
        if not res.status_code == 200:
            raise exceptions.ValidationError('微服务发生错误，返回非200类消息')
        if res.json()['code'] != 0:
            raise exceptions.ValidationError('验证错误: %s' % res.json()['msg'])
        return res.json()['data']


class AuthorizeServer:
    """认证服务"""

    @staticmethod
    def ticket_authorize(ticket):
        """ticket认证"""
        url = "%s/api/common/auth/authorize/" % micro_service_domain
        params = {'ticket': ticket}
        res = BaseHttpServer.get(url=url, params=params)
        return res

    @staticmethod
    def create_ticket(user_id):
        """通过user_id创建ticket"""
        url = "%s/api/common/auth/authorize/" % micro_service_domain
        json_data = {'user_id': user_id}
        data = BaseHttpServer.post(url=url, json_data=json_data)
        return data['ticket']

    @staticmethod
    def delete_ticket(ticket):
        """删除ticket"""
        url = "%s/api/common/auth/authorize/" % micro_service_domain
        params = {'ticket': ticket}
        data = BaseHttpServer.get(url, params)
        return data


class WeixinServer:
    """微信公众号服务"""

    @staticmethod
    def get_access_token():
        """获取access_token"""
        url = "%s/api/weixin/service_center/access_token/" % micro_service_domain
        params = {}
        data = BaseHttpServer.get(url, params)
        return data

    @staticmethod
    def send_text_message(openid, content):
        """发送文本消息"""
        json_data = {
            'openid': openid,
            'content': content
        }
        url = "%s/api/weixin/service_center/send_text_message/" % micro_service_domain
        data = BaseHttpServer.post(url, json_data)
        return data

    @staticmethod
    def send_template_message(openid, template_id, url, send_data):
        """发送模板消息"""
        json_data = {
            'openid': openid,
            'template_id': template_id,
            'url': url,
            'send_data': send_data
        }
        url = "%s/api/weixin/service_center/send_template_message/" % micro_service_domain
        data = BaseHttpServer.post(url, json_data)
        return data

    @staticmethod
    def code_authorize(code):
        """通过code获取网页授权"""
        url = "%s/api/weixin/service_center/code_authorize/" % micro_service_domain
        params = {'code': code}
        data = BaseHttpServer.get(url, params)
        return data

    @staticmethod
    def get_web_user_info(openid, access_token):
        """获取网页授权用户信息"""
        url = "%s/api/weixin/service_center/get_web_user_info/" % micro_service_domain
        data = BaseHttpServer.get(url, {'openid': openid, 'access_token': access_token})
        return data

    @staticmethod
    def get_temporary_qr_code(action_name, scene_id, expired_time=7*24*60*60):
        """获取临时二维码"""
        url = "%s/api/weixin/service_center/temporary_qr_code/" % micro_service_domain
        json_data = {
            "action_name": action_name,
            "scene_id": scene_id,
            "expired_time": expired_time
        }
        data = BaseHttpServer.post(url, json_data)
        return data['qr_img_url']

    @staticmethod
    def get_forever_qr_code(action_name, scene_id):
        """获取永久二维码"""
        url = "%s/api/weixin/service_center/forever_qr_code/" % micro_service_domain
        json_data = {
            "action_name": action_name,
            "scene_id": scene_id,
        }
        data = BaseHttpServer.post(url, json_data)
        return data['qr_img_url']


