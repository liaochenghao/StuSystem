# coding: utf-8
from rest_framework import serializers
from utils.serializer_fields import VerboseChoiceField


class CommonNoticeSerializer(serializers.Serializer):
    MODULE_NAME = (
        ('project', '项目模块'),
        ('order', '订单模块'),
        ('course', '课程模块'),
        ('course_confirm', '审核课程'),
        ('course_score', '课程成绩'),
        ('course_switch', '学分转换')
    )
    module_name = VerboseChoiceField(choices=MODULE_NAME)
