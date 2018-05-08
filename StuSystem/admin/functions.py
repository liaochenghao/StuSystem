# coding: utf-8
import datetime
import qrcode
from urllib import parse

import xlwt
from django.http import HttpResponse
from rest_framework import exceptions

from StuSystem.settings import DOMAIN, MEDIA_ROOT, MEDIA_URL, WX_SMART_PROGRAM
from authentication.models import UserInfo
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
            'create_time': user_instance.create_time
        }
    else:
        channel = None

    return channel


def change_student_status(user_id, status):
    student_instance = UserInfo.objects.filter(user_id=user_id).first()
    student_instance.student_status = status
    student_instance.save()
    return


def make_qrcode(channel_id):
    auth_domain = 'http://apply.chinasummer.org'
    redirect_uri = parse.quote('%s/?channel_id=%s' % (auth_domain, channel_id))
    channel_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' % (
        WX_SMART_PROGRAM['APP_ID'], redirect_uri)
    channel_img = qrcode.make(channel_url)
    qr_code_save_path = '%s%s%s%s' % (MEDIA_ROOT, '/common/channel/channel_', channel_id, '.jpg')
    qr_code_url = '%s%s%s%s%s' % (DOMAIN, MEDIA_URL, 'common/channel/channel_', channel_id, '.jpg')
    channel_img.save(qr_code_save_path)
    return (qr_code_url, channel_url)


def get_chose_number(project):
    course_queryset = UserCourse.objects.filter(project=project).distinct().values('course__name', 'course')
    if not course_queryset:
        raise exceptions.NotAuthenticated('项目ID错误 ！')
    write_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    first_sheet = write_book.add_sheet('课程选课人数', cell_overwrite_ok=True)
    second_sheet = write_book.add_sheet('选课人数', cell_overwrite_ok=True)
    col_list = ['校区-项目', '课程', '人数', '姓名', 'CC', '邮箱', '微信']
    for index, col in enumerate(col_list):
        first_sheet.write(0, index, col)
        second_sheet.write(0, index, col)
    first_row = 1
    second_row = 1
    user_list = []
    for course in course_queryset:
        userinfo_set = UserCourse.objects.filter(project=project, course_id=course['course']).values(
            'user__userinfo__name', 'user__userinfo__sales_man', 'user__userinfo__email',
            'user__userinfo__wechat')
        course_count = len(userinfo_set)
        if course_count == 0:
            continue
        user_bool = 1
        for item in userinfo_set:
            if item.get('user__userinfo__name') == '123':
                continue
            # 第一张表
            first_sheet.write(first_row, 0, project.campus.name + '-' + project.name)
            first_sheet.write(first_row, 1, course['course__name'])
            if user_bool == 1:
                second_sheet.write(second_row, 2, course_count)
            first_sheet.write(first_row, 3, item.get('user__userinfo__name'))
            first_sheet.write(first_row, 4, item.get('user__userinfo__sales_man'))
            first_sheet.write(first_row, 5, item.get('user__userinfo__email'))
            first_sheet.write(first_row, 6, item.get('user__userinfo__wechat'))
            # 第二张表
            if not item.get('user__userinfo__wechat') in user_list:
                user_list.append(item.get('user__userinfo__wechat'))
                second_sheet.write(second_row, 0, project.campus.name + '-' + project.name)
                second_sheet.write(second_row, 1, course['course__name'])
                if user_bool == 1:
                    second_sheet.write(second_row, 2, course_count)
                second_sheet.write(second_row, 3, item.get('user__userinfo__name'))
                second_sheet.write(second_row, 4, item.get('user__userinfo__sales_man'))
                second_sheet.write(second_row, 5, item.get('user__userinfo__email'))
                second_sheet.write(second_row, 6, item.get('user__userinfo__wechat'))
                second_row += 1
            first_row += 1
            user_bool = 0
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment;filename="course.xlsx"'
    write_book.save(response)
    return response


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
