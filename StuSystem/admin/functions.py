# coding: utf-8
import datetime

from market.models import Channel
from utils.weixin_client import wx_client


def get_channel_info(user_info_instance):
    if user_info_instance.channel_id and Channel.objects.filter(id=user_info_instance.channel_id).exists():
        channel_instance = Channel.objects.get(id=user_info_instance.channel_id)
        channel = {
            'id': channel_instance.id,
            'name': channel_instance.name,
            'create_time': channel_instance.create_time
        }
    else:
        channel_instance = Channel.objects.filter(userchannel__openid=user_info_instance.openid).first()
        if channel_instance:
            channel = {
                'id': channel_instance.id,
                'name': channel_instance.name,
                'create_time': channel_instance.create_time
            }
        else:
            channel = None

    return channel


def order_confirmed_template_message(openid, name, confirm_status, remark):
    data = {
        'first': '您的订单有新的审核反馈啦',
        'keyword1': '',  # 姓名
        'keyword2': '',  # 日期
        'keyword3': '',  # 审核结果
        'remark': ''  # remark
    }
    data['keyword1'] = name
    data['keyword2'] = datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')
    data['keyword3'] = confirm_status
    data['remark'] = remark
    templates_id = 'fOjcVFfvIL2XBGif0uI2-2SVZGMRI7foq3zYCIK4c8U'
    url = ''
    res = wx_client.template_send(openid, templates_id, url, **data)
    return


if __name__ == '__main__':
    order_confirmed_template_message(openid='oAKoA0_Pps0xXJSuRZPtkA_NI3jg',
                                     name='邱雷',
                                     confirm_status='审核成功',
                                     remark='您的订单审核成功，请联系您的课程顾问，开始选课吧！')