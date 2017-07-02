# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rest_framework.response import Response
from weixin_server.client import client
from authentication.models import User, UserInfo
from authentication.functions import UserTicket
import datetime


def view(request):
    # code = request.GET.get('code')
    # res = client.get_web_access_token(code)
    # if not (res.get('access_token') and res.get('openid')):
    #     return render_to_response('error.html')
    # todo
    # res = {
    #     "openid": "qwertyuiop123456",
    # }
    #
    # user_info = {
    #     "nickname": "22222211",
    #     "headimgurl": "http://www.baidu.com/abcdef/edfg/asdf/",
    #     "unionid": "qweasdfzxcv"
    # }
    # user_info = client.get_web_user_info(res['access_token'], res['openid'])
    # user, created = User.objects.get_or_create(**{'username': res['openid'], 'role': 'STUDENT'})
    # ticket = UserTicket.create_ticket(user)
    # user.last_login = datetime.datetime.now()
    # user.save()
    # UserInfo.objects.update_or_create(defaults={'openid': res['openid']},
    #                                                        **{
    #                                                            "user": user,
    #                                                            "unionid": user_info.get('unionid'),
    #                                                            "headimgurl": user_info['headimgurl'],
    #                                                            "openid": res['openid'],
    #                                                            "wx_name": user_info['nickname']
    #                                                        })
    # response = render_to_response('index.html')
    # response.set_cookie('ticket', ticket)
    return render_to_response('index.html')