# coding: utf-8
import json, datetime
from werobot.client import Client
import requests
from StuSystem.settings import WX_CONFIG

from utils.redis_server import redis_client


class WeiXinClient(Client):

    def get_grant_token(self):
        """获取微信access_token"""
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            WX_CONFIG['APP_ID'], WX_CONFIG['APP_SECRET'])
        res = requests.get(url)
        res_data = res.json()
        redis_client.set_instance('access_token', res_data['access_token'], default_valid_time=(2*60*60 - 100))
        return res_data['access_token']

    def get_valid_access_token(self):
        cached_access_token = redis_client.get_instance('access_token', False)
        if not cached_access_token:
            cached_access_token = self.get_grant_token()
        return cached_access_token

    def send_text_message(self, openid, content):
        """发送文本消息"""
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send"
        querystring = {
            "access_token": self.get_valid_access_token()}

        payload = ("{\"touser\": \"%s\", \"msgtype\": \"text\",  \"text\": {\"content\": \"%s\" }}" % (openid, content)).encode('utf-8')
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "3a32082a-0052-5591-5a7e-bf815defb396"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response.json()

    def template_send(self, open_id, template_id, url, topcolor="#FF0000", **kwargs):
        """
        发送模板消息
        """
        data = {}

        for key, value in kwargs.items():
            # 转换成微信要求格式
            data[key] = {
                'value': value,
                'color': '#173177'
            }
        post_data = {
            'touser': open_id,
            'template_id': template_id,
            'url': url,
            'data': data
        }
        base_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='

        url = base_url + self.get_access_token()
        res = requests.post(url=url, data=json.dumps(post_data), headers={'Content-Type': 'application/json'}).json()
        if not res.get('errcode') or res.get('errcode') == 0:  # 如果access_token有效
            return res
        else:
            url = base_url + self.get_access_token()
            res = requests.post(url=url, data=json.dumps(post_data), headers={'Content-Type': 'application/json'}).json()
        return res

    def upload_medias(self, media_type, media_file, openid):
        """上传图片"""
        access_token = self.token
        url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (access_token, media_type)
        res = requests.post(url, files={"media": open(media_file, "rb")})
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
        data = {
            "touser": openid,
            "msgtype": "image",
            "image": {
                "media_id": res.json().get('media_id', 'error_occur')
            }
        }
        requests.post(url=url, json=data)
        return