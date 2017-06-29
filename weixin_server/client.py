# coding: utf-8
from werobot.client import Client
from django.conf import settings
import requests


class WxClient(Client):
    def __init__(self):
        self.config = settings.WX_CONFIG
        self._token = None
        self.token_expires_at = None
    #     super().__init__(self.config)

    def get_web_access_token(self, code):
        """
        微信网页认证code获取access_token
        :return: {
            "access_token":"ACCESS_TOKEN",
             "expires_in":7200,
             "refresh_token":"REFRESH_TOKEN",
             "openid":"OPENID",
             "scope":"SCOPE"
         }
        """
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        params = {
            "appid": settings.WX_CONFIG["APP_ID"],
            "secret": settings.WX_CONFIG["APP_SECRET"],
            "code": code,
            "grant_type": "authorization_code"
        }
        res = requests.get(url, params=params).json()
        return res

    def refresh_web_access_token(self, refresh_token):
        """
        刷新网页获取的access_token
        :return: {
            "access_token":"ACCESS_TOKEN",
            "expires_in":7200,
            "refresh_token":"REFRESH_TOKEN",
            "openid":"OPENID",
            "scope":"SCOPE"
        }
        """
        url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        params = {
            "appid": settings.WX_CONFIG['APP_ID'],
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        res = requests.get(url, params=params).json()
        return res

    def get_web_user_info(self, access_token, openid):
        """
        通过openid获取网页授权的用户信息
        :param openid:
        :return: {
            "openid":" OPENID",
            "nickname": NICKNAME,
            "sex":"1",                                   用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
            "province":"PROVINCE"
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl": "",
            "privilege":["PRIVILEGE1" "PRIVILEGE2"],     用户特权信息，json 数组，如微信沃卡用户为（chinaunicom）
            "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"   只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
        }
        """
        url = "https://api.weixin.qq.com/sns/userinfo"
        params = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN"
        }
        res = requests.get(url, params=params).json()
        return res

    def check_web_access_token(self, access_token, openid):
        """
        校验网页授权access_token是否有效
        :param access_token:
        :return: {
            "errcode":0,
            "errmsg":"ok"
        }
        """
        url = "https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID"
        params = {
            "access_token": access_token,
            "openid": openid
        }
        res = requests.get(url, params=params).json()
        return res

client = WxClient()