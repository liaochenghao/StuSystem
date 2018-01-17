# coding: utf-8
import datetime
import json

from authentication.functions import auto_assign_sales_man
from common.models import SalesManUser, SalesMan
from rest_framework import serializers

from authentication.models import User, UserInfo, StudentScoreDetail
from utils.serializer_fields import VerboseChoiceField
from micro_service.service import AuthorizeServer, WeixinServer


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField()

    class Meta:
        model = User
        exclude = ['password', 'is_active']


class CreateAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
    ticket = serializers.CharField(required=False, allow_null=True)

    def check_account(self, validated_data):

        if validated_data.get('ticket'):
            ticket_authorize = AuthorizeServer.ticket_authorize(validated_data['ticket'])
            if ticket_authorize['valid_ticket']:
                user = User.objects.get(id=ticket_authorize['user_id'])
                student_info = UserInfo.objects.filter(user=user).first()
                ticket = validated_data['ticket']
            else:
                user, student_info, ticket = self.weixin_authorize(validated_data)
        else:
            user, student_info, ticket = self.weixin_authorize(validated_data)
            # 自动分配课程顾问
            auto_assign_sales_man(user)

        if all([student_info.name, student_info.email, student_info.wechat, student_info.wcampus]) is False:
            need_complete_stu_info = True
        else:
            need_complete_stu_info = False
        return {'need_complete_student_info': need_complete_stu_info, 'user_id': user.id, 'ticket': ticket,
                'valid_sales_man': True if student_info.valid_sales_man else False}

    def weixin_authorize(self, validated_data):
        res = WeixinServer.code_authorize(validated_data['code'])
        if not (res.get('access_token') and res.get('openid')):
            raise serializers.ValidationError('无效的code值, 微信网页认证失败')
        user_info = WeixinServer.get_web_user_info(access_token=res['access_token'], openid=res['openid'])
        if user_info.get('errorcode', 0) != 0:
            raise serializers.ValidationError('user info 获取错误')
        # 创建用户
        user = User.objects.filter(username=user_info.get('unionid')).first()
        if not user:
            user = User.objects.create(**{
                'username': user_info.get('unionid'),
                'role': 'STUDENT',
                'openid': res['openid'],
                'unionid': user_info.get('unionid')
            })
        ticket = AuthorizeServer.create_ticket(user.id)
        user.last_login = datetime.datetime.now()
        user.save()

        # 创建用户信息
        student_info = UserInfo.objects.filter(user=user).first()
        if not student_info:
            student_info = UserInfo.objects.create(user=user)
        student_info.unionid = user_info.get('unionid')
        student_info.openid = res['openid']
        student_info.headimgurl = user_info['headimgurl']
        student_info.wx_name = user_info['nickname']
        student_info.save()
        return user, student_info, ticket


class AssignSalesManSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)

    def create(self, validated_data):
        res = WeixinServer.code_authorize(validated_data['code'])
        if not (res.get('access_token') and res.get('openid')):
            raise serializers.ValidationError('无效的code值, 微信网页认证失败')
        weixin_info = WeixinServer.get_web_user_info(res['access_token'], res['openid'])
        user, created = User.objects.get_or_create(**{
            'username': weixin_info.get('unionid'),
            'role': 'STUDENT',
            'openid': res['openid'],
            'unionid': weixin_info.get('unionid')
        })

        ticket = AuthorizeServer.create_ticket(user.id)
        user.last_login = datetime.datetime.now()
        user.save()
        UserInfo.objects.update_or_create(defaults={'openid': res['openid']},
                                          **{
                                               "user": user,
                                               "unionid": weixin_info.get('unionid'),
                                               "headimgurl": weixin_info['headimgurl'],
                                               "openid": res['openid'],
                                               "wx_name": weixin_info['nickname']
                                           })
        sales_man_info = auto_assign_sales_man(user)
        return {'sales_man': sales_man_info, 'ticket': ticket}


class UserInfoSerializer(serializers.ModelSerializer):
    wcampus = serializers.ListField(write_only=True)

    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'wechat', 'wcampus', 'cschool', 'headimgurl', 'valid_sales_man']
        read_only_fields = ['headimgurl']

    def validate(self, attrs):
        if attrs.get('wcampus'):
            attrs['wcampus'] = json.dumps(attrs['wcampus'])
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['wcampus'] = json.loads(instance.wcampus) if instance.wcampus else []
        return data


# 兼容微信小程序客户端
class CustomUserInfoSerializer(serializers.ModelSerializer):
    wcampus = serializers.ListField()

    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'wechat', 'wcampus', 'cschool', 'headimgurl', 'valid_sales_man']
        read_only_fields = ['headimgurl']

    def validate(self, attrs):
        try:
            if attrs.get('wcampus'):
                # attrs['wcampus'] = json.dumps(attrs['wcampus'][0].split(','))
                attrs['wcampus'] = json.dumps(attrs['wcampus'])
        except Exception as e:
            raise serializers.ValidationError('wcampus验证错误: %s' % e)
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['wcampus'] = json.loads(instance.wcampus) if instance.wcampus else []
        return data


class ListUserInfoSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(source='user.last_login')

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'cschool', 'last_login']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        personal_file = any([instance.first_name, instance.last_name, instance.gender, instance.id_number,
                             instance.major, instance.graduate_year, instance.gpa])     # 判断用户是否已建档
        data['personal_file'] = '已建档' if personal_file else '未建档'
        return data


class PersonalFIleUserInfoSerializer(serializers.ModelSerializer):
    """用户档案Serializer"""
    gender = VerboseChoiceField(choices=UserInfo.GENDER)
    # todo 暂时将grade, birth_date, phone 设置为非必要参数
    grade = VerboseChoiceField(choices=UserInfo.GRADE, required=False)
    birth_date = serializers.DateField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'wechat', 'cschool', 'first_name', 'last_name', 'gender', 'id_number',
                  'major', 'graduate_year', 'gpa', 'birth_date', 'grade', 'phone']
        read_only_fields = ['id', 'name', 'email', 'wechat', 'cschool']


class StudentScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScoreDetail
        fields = ['id', 'user', 'department', 'phone', 'country', 'post_code', 'address']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SalesManUserSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    sales_man = serializers.IntegerField()

    def validate(self, attrs):
        user = attrs['user']
        if SalesManUser.objects.filter(user=user).exists():
            raise serializers.ValidationError('已有关联的销售顾问')
        if not SalesMan.objects.filter(id=attrs['sales_man']).exists():
            raise serializers.ValidationError('销售人员不存在')
        return attrs

    def create(self, validated_data):
        instance = SalesManUser.objects.create(**{'user_id': validated_data['user'],
                                                  'sales_man_id': validated_data['sales_man']})
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=6, max_length=30)
    password = serializers.CharField(min_length=6, max_length=30)

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('用户名不存在')
        user = User.objects.get(username=attrs['username'])
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise serializers.ValidationError('该用户已被禁用')
        self.user = user
        return attrs

    def create_ticket(self):
        ticket = AuthorizeServer.create_ticket(self.user.id)
        self.user.last_login = datetime.datetime.now()
        self.user.save()
        return {'msg': '登录成功', 'user_id': self.user.id, 'ticket': ticket, 'role': self.user.role}


class ClientAuthorizeSerializer(serializers.Serializer):
    code = serializers.CharField()