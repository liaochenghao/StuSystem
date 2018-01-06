# coding: utf-8
import datetime
import json

import requests
from rest_framework import exceptions
from StuSystem.settings import WX_CONFIG
from authentication.functions import UserTicket
from authentication.models import User


class WxSmartProgram:

    def __init__(self):
        self.appid = WX_CONFIG['appid']
        self.secret = WX_CONFIG['secret']

    def code_authorize(self, code):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get(url=url, params=params)
        if response.status_code != 200:
            raise exceptions.ValidationError('connecting wechat server error')
        res = response.json()
        # res = {'openid': 'oU9IT0QXc0ZoIz2xbG7mYr2GdAXA', "session_key": "tiihtNczf5v6AKRyjwEUhQ=="}
        if res.get('openid') and res.get('session_key'):
            user, created = User.objects.get_or_create(username=res['openid'])
            user.last_login = datetime.datetime.now()
            user.session_key = res['session_key']
            user.save()
            ticket = UserTicket.create_ticket(user)
            return {'user_id': user.id, 'ticket': ticket}
        else:
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxSmartProgram = WxSmartProgram()