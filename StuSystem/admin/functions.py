# coding: utf-8
import datetime
import qrcode
from urllib import parse

from StuSystem.settings import DOMAIN, MEDIA_ROOT, MEDIA_URL, WX_SMART_PROGRAM
from market.models import Channel
from order.models import UserCourse, Order
from utils.future_help import run_on_executor
from micro_service.service import WeixinServer
from EventAggregator.event_aggregator import EventAggregator
from micro_service.stores.message_auto_notice import MessageAutoNotice


def get_channel_info(user_instance):
    if user_instance.channel_id and Channel.objects.filter(id=user_instance.channel_id).exists():
        channel_instance = Channel.objects.get(id=user_instance.channel_id)
        channel = {
            'id': channel_instance.id,
            'name': channel_instance.name,
            'create_time': channel_instance.create_time
        }
    else:
        channel = None

    return channel


def make_qrcode(channel_id):
    auth_domain = 'http://su.chinasummer.org'
    redirect_uri = parse.quote('%s?channel_id=%s' % (auth_domain, channel_id))
    channel_img = qrcode.make('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' % (
            WX_SMART_PROGRAM['APP_ID'], redirect_uri))
    qr_code_save_path = '%s%s%s%s' % (MEDIA_ROOT, '/common/channel/channel_', channel_id, '.jpg')
    qr_code_url = '%s%s%s%s%s' % (DOMAIN, MEDIA_URL, 'common/channel/channel_', channel_id, '.jpg')
    channel_img.save(qr_code_save_path)
    return qr_code_url


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
    WeixinServer.send_template_message(openid, template_id, url, **data)
    return


@run_on_executor
def create_course_template_message(openid, user_name, sales_man_name, project_name, course_name, course_time, address):
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
    data['first'] = 'Hi【%s】，你的课程顾问【%s】刚刚为你的项目【%s】注册了课程\n' % (user_name, sales_man_name, project_name)
    data['keyword1'] = course_name
    data['keyword2'] = course_time
    data['remark'] = '上课地点: %s\n\n请尽快确认所选课程，若所选课程有误，请立即与您的专属课程顾问联系，更改课程！' % address
    WeixinServer.send_template_message(openid, templates_id, url, **data)
    return


@run_on_executor
def order_auto_notice_message(order, user):
    """缴费审核通知"""
    data = {
        'user_id': user['id'],
        'module_name': 'order',
        'msg': '您有一条订单%s，订单号为:%d' % (order.get('status')['verbose'], order.get('id'))
    }
    EventAggregator.publish(MessageAutoNotice(**data))


@run_on_executor
def course_auto_notice_message(instance):
    """管理员新增课程通知"""
    data = {
        'user_id': instance.user_id,
        'module_name': 'course',
        'msg': '您新增了一门课程:%s' % instance.course.name
    }
    EventAggregator.publish(MessageAutoNotice(**data))


@run_on_executor
def confirm_auto_notice_message(usercourse, user):
    """课程审核通知"""
    data = {
        'user_id': user.id,
        'module_name': 'course_confirm',
        'msg': '您有一门课程:%s,审核%s' % (usercourse.course.name, dict(UserCourse.STATUS).get(usercourse.status))
    }
    EventAggregator.publish(MessageAutoNotice(**data))


@run_on_executor
def score_auto_notice_message(course, user):
    """课程成绩通知"""
    data = {
        'user_id': user['user'],
        'module_name': 'scores',
        'msg': '您有一门课程:%s,成绩已提交' % course.get('name')
    }
    EventAggregator.publish(MessageAutoNotice(**data))


@run_on_executor
def switch_auto_notice_message(user, course, status):
    """学分转换通知"""
    data = {
        'user_id': user['id'],
        'module_name': 'credit_switch',
        'msg': '您有一门课程:%s,%s' % (course.get('name'), status.get('verbose'))
    }
    EventAggregator.publish(MessageAutoNotice(**data))


@run_on_executor
def coupon_auto_notice_message(instance):
    """新增优惠券通知"""
    data = {
        'user_id': instance.data.get('user'),
        'module_name': 'coupon',
        'msg': '您获得了新的优惠卷'
    }
    EventAggregator.publish(MessageAutoNotice(**data))
