# coding: utf-8
import datetime
import json

import requests
from rest_framework import exceptions
from StuSystem.settings import WX_SMART_PROGRAM
from micro_service.service import AuthorizeServer
from authentication.models import User, UserInfo


class WxSmartProgram:

    def __init__(self):
        self.appid = WX_SMART_PROGRAM['APP_ID']
        self.secret = WX_SMART_PROGRAM['APP_SECRET']

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
        # res = {'openid': 'oAKoA03ardxfbwr8gO-FCHnG11', "session_key": "tiihtNczf5v6AKRyjwEUhQ=="}
        if res.get('openid') and res.get('session_key') and res.get('unionid'):
            user = User.objects.filter(username=res['unionid']).first()
            if not user:
                user = User.objects.create(username=res['unionid'], role='STUDENT', s_openid=res['openid'], openid=None,
                                           unionid=res['unionid'])
            user.s_openid = res['openid']
            ticket = AuthorizeServer.create_ticket(user.id)
            user.last_login = datetime.datetime.now()
            user.save(update_fields=['s_openid', 'last_login'])
            user_info = UserInfo.objects.filter(user=user).first()
            if not user_info:
                user_info = UserInfo.objects.create(user=user, s_openid=res['openid'], unionid=res['unionid'], openid=None)
            user_info.s_openid = res['openid']
            user_info.save(update_fields=['s_openid'])
            return {'user_id': user.id, 'ticket': ticket}
        else:
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxSmartProgram = WxSmartProgram()