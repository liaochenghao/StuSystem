# coding: utf-8
import datetime
import json

import requests
from rest_framework import exceptions
from StuSystem.settings import WX_CONFIG
from authentication.functions import UserTicket
from authentication.models import User, UserInfo


class WxSmartProgram:

    def __init__(self):
        self.appid = WX_CONFIG['APP_ID']
        self.secret = WX_CONFIG['APP_SECRET']

    def code_authorize(self, code):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        # response = requests.get(url=url, params=params)
        # if response.status_code != 200:
        #     raise exceptions.ValidationError('connecting wechat server error')
        # res = response.json()
        res = {'openid': 'oAKoA03ardxfbwr8gO-FCHnG9Wv02112', "session_key": "tiihtNczf5v6AKRyjwEUhQ=="}
        if res.get('openid') and res.get('session_key'):
            user, created = User.objects.get_or_create(**{'username': res['openid'], 'role': 'STUDENT'})
            ticket = UserTicket.create_ticket(user)
            user.last_login = datetime.datetime.now()
            user.save()
            student_info, created = UserInfo.objects.update_or_create(defaults={'openid': res['openid']},
                                                                      **{
                                                                          "user": user,
                                                                          "openid": res['openid']
                                                                      })
            return {'user_id': user.id, 'ticket': ticket}
        else:
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxSmartProgram = WxSmartProgram()