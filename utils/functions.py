# coding: utf-8
from weixin_server.client import client


def get_key_verbose_data(data: dict):
    """将dict数据结构变为key,verbose的list"""
    res = []
    for key, value in data.items():
        res.append({'key': key, 'verbose': value}),
    return res


def get_long_qr_code(key):
    """根据key值获取永久二维码"""
    data = {
        'action_name': 'QR_LIMIT_STR_SCENE',
        'action_info': {
            'scene': {'scene_str': key}
        }
    }
    res = client.create_qrcode(data)
    qr_code = ''
    if res.get('url') and res.get('ticket'):
        qr_code = client.show_qrcode(res['ticket']).url
    return qr_code


# def get_temporary_qr_code(key):
#     """获取临时二维码，默认7天有效"""
#     access_token =
#     url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=' %
#     data = {
#         "expire_seconds": 7 * 24 * 3600,
#         "action_name": "QR_SCENE",
#         "action_info": {
#             "scene": {
#                 "scene_id": 123
#             }
#         }
#     }