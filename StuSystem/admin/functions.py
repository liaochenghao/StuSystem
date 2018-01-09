# coding: utf-8
import datetime

from market.models import Channel
from weixin_server.weixin_client import wx_client
from utils.future_help import run_on_executor


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


@run_on_executor
def order_confirmed_template_message(openid, name, confirm_status, remark):
    """订单确认模板消息"""
    template_id = 'fOjcVFfvIL2XBGif0uI2-2SVZGMRI7foq3zYCIK4c8U'
    data_template = {
        'first': '您的订单有新的审核反馈啦',
        'keyword1': '',  # 姓名
        'keyword2': '',  # 日期
        'keyword3': '',  # 审核结果
        'remark': ''  # remark
    }
    data = data_template
    data['keyword1'] = name
    data['keyword2'] = datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')
    data['keyword3'] = confirm_status
    data['remark'] = remark
    url = ''
    res = wx_client.template_send(openid, template_id, url, **data)
    return


@run_on_executor
def create_course_template_message(openid, user_name, sales_man_name, project_name, course_name, address):
    """创建课程通知消息"""
    templates_id = 'BmuykpTx7GVgJMmc33Wmh54ukw_s_sx3j9H2gum5Mww'
    url = ''
    data_template = {
        'first': '',
        'keyword1': '',
        'keyword2': '',
        'remark': ''
    }
    data = data_template
    data['first'] = 'Hi【%s】，你的课程顾问【%s】刚刚为你的项目【%s】注册了课程' % (user_name, sales_man_name, project_name)
    data['keyword1'] = course_name
    data['keyword2'] = address
    data['remark'] = '若所选课程有误，请立即与您的专属课程顾问联系，更改课程！'
    wx_client.template_send(openid, templates_id, url, data)
    return


if __name__ == '__main__':
    # order_confirmed_template_message(openid='oAKoA0_Pps0xXJSuRZPtkA_NI3jg',
    #                                  name='邱雷',
    #                                  confirm_status='审核成功',
    #                                  remark='您的订单审核成功，请联系您的课程顾问，开始选课吧！')
    create_course_template_message(openid='oAKoA0_Pps0xXJSuRZPtkA_NI3jg',
                                   user_name='邱雷',
                                   sales_man_name='yirantai',
                                   project_name='上海校区五周项目',
                                   course_name='Financial Accounting',
                                   address='武汉理工大学')