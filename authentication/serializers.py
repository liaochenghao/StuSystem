# coding: utf-8
from rest_framework import serializers
from weixin_server.client import client
from .models import User, UserInfo
from .functions import UserTicket
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
        res = client.get_web_access_token(validated_data['code'])
        user_info = client.get_web_user_info(res['access_token'], res['openid'])
        if not UserInfo.objects.filter(openid=res['openid']).exists():
            user = User.objects.create(**{'username': res['openid'], 'role': 'STUDENT'})
            UserInfo.objects.create(**{
                "user": user,
                "unionid": user_info.get('unionid'),
                "headimgurl": user_info['headimgurl'],
                "openid": res['openid'],
                "wx_name": user_info['nickname']
            })
            need_complete_stu_info = True
        else:
            user = UserInfo.objects.get(openid=res['openid'])
            if any([user.name, user.email, user.wechat, user.school, user.wcampus]) is False:
                need_complete_stu_info = True
            else:
                need_complete_stu_info = False
        return {'need_complete_stu_info': need_complete_stu_info, 'user_id': user.id}


class UserInfoSerializer(serializers.ModelSerializer):
    wcampus = serializers.ListField()
    wschool = serializers.ListField()

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
        data['wcampus'] = json.loads(instance.wcampus)
        data['wschool'] = json.loads(instance.wschool)
        return data


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