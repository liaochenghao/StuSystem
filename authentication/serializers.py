# coding: utf-8
from rest_framework import serializers
from weixin_server.client import client
from utils.serializer_fields import VerboseChoiceField
from authentication.models import User, UserInfo, UserScoreDetail
from course.models import Campus
from authentication.functions import UserTicket
from common.models import SalesManUser, SalesMan
from coupon.models import Coupon
import datetime
import json


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField()

    class Meta:
        model = User
        exclude = ['password', 'delete', 'is_active']


class CreateAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)

    def check_account(self, validated_data):
        # res = client.get_web_access_token(validated_data['code'])
        # user_info = client.get_web_user_info(res['access_token'], res['openid'])
        # todo debug
        res = {
            "openid": "kldjflkajdlkjdlkf",
        }

        user_info = {
            "nickname": "woshichenguanxi",
            "headimgurl": "http://www.qq.com",
            "unionid": "124dajldjflkadjfdkjfa"
        }
        user = User.objects.get_or_create(**{'username': res['openid'], 'role': 'STUDENT'})
        if not UserInfo.objects.filter(openid=res['openid']).exists():
            UserInfo.objects.create(**{
                "user": user,
                "unionid": user_info.get('unionid'),
                "headimgurl": user_info['headimgurl'],
                "openid": res['openid'],
                "wx_name": user_info['nickname']
            })
            need_complete_stu_info = True
        else:
            UserInfo.objects.filter(openid=res['openid']).update(**{
                "unionid": user_info.get('unionid'),
                "headimgurl": user_info['headimgurl'],
                "wx_name": user_info['nickname']
            })
            user_info = UserInfo.objects.get(openid=res['openid'])
            if any([user_info.name, user_info.email, user_info.wechat, user_info.wschool, user_info.wcampus]) is False:
                need_complete_stu_info = True
            else:
                need_complete_stu_info = False
        return {'need_complete_stu_info': need_complete_stu_info, 'user_id': user.id}


class UserInfoSerializer(serializers.ModelSerializer):
    wcampus = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    wschool = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'wechat', 'wschool', 'wcampus', 'cschool']

    def validate(self, attrs):
        if attrs.get('wschool'):
            attrs['wschool'] = json.dumps(attrs['wschool'])
        if attrs.get('wcampus'):
            attrs['wcampus'] = json.dumps(attrs['wcampus'])
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        campus_list = Campus.objects.filter(id__in=json.loads(instance.wcampus)).values_list('name', flat=True)
        data['wcampus'] = campus_list
        data['wschool'] = json.loads(instance.wschool)
        return data


class PersonalFIleUserInfoSerializer(serializers.ModelSerializer):
    gender = VerboseChoiceField(choices=UserInfo.GENDER)

    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'wechat', 'cschool', 'first_name', 'last_name', 'gender', 'id_number',
                  'major', 'graduate_year', 'gpa']
        read_only_fields = ['id', 'name', 'email', 'wechat', 'cschool']


class UserScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScoreDetail
        fields = ['id', 'user', 'department', 'phone', 'country', 'post_code', 'address']

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
        ticket = UserTicket.create_ticket(self.user)
        self.user.last_login = datetime.datetime.now()
        self.user.save()
        return {'msg': '登录成功', 'user_id': self.user.id, 'ticket': ticket}
