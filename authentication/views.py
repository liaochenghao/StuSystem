# coding: utf-8
import random
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework import exceptions
from authentication.models import User, UserInfo, UserScoreDetail
from coupon.models import Coupon
from common.models import SalesMan, SalesManUser
from authentication.functions import UserTicket
from authentication.serializers import UserSerializer, ListUserInfoSerializer, LoginSerializer, CreateAccountSerializer, \
    UserInfoSerializer, PersonalFIleUserInfoSerializer, UserScoreDetailSerializer, SalesManUserSerializer
from authentication.filters import UserInfoFilterSet


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer

    @list_route(['POST'], serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.create_ticket()
        response = Response(res)
        response.set_cookie('ticket', res.get('ticket'))
        return response

    @list_route(['GET'], serializer_class=CreateAccountSerializer)
    def check_account(self, request):
        # 检查账户信息
        data = self.request.query_params.dict()
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            ticket = request.GET.get('ticket')
        data['ticket'] = ticket
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        res = serializer.check_account(serializer.validated_data)
        response = Response(res)
        response.set_cookie('ticket', res.get('ticket'))
        return response

    @list_route()
    def check_user_info(self, request):
        user = request.user
        user_info = UserInfo.objects.filter(user=user).first()
        if not user_info:
            raise exceptions.ValidationError('不存在基础的用户信息')
        if any([user_info.name, user_info.email, user_info.wechat, user_info.wschool, user_info.wcampus]) is False:
            need_complete_stu_info = True
        else:
            need_complete_stu_info = False
        return Response({'need_complete_stu_info': need_complete_stu_info, 'user_id': user.id})

    @list_route(['put'])
    def logout(self, request):
        """ 退出登录
        """
        ticket = request.COOKIES.get('ticket')
        UserTicket.delete_ticket(ticket)
        ret_data = {'msg': '退出登录成功'}
        return Response(ret_data)

    @detail_route()
    def coupon_list(self, request, pk):
        """
        获取用户优惠券
        :param request:
        :return:
        """
        user = request.user
        res = Coupon.objects.filter(usercoupon__user=user, usercoupon__used=False).values(
            'id', 'code', 'amount', 'info', 'start_time', 'end_time')
        return Response(res)

    @detail_route(['GET', 'POST'], serializer_class=SalesManUserSerializer)
    def sales_man(self, request, pk):
        """
        获取销售人员信息
        """
        user = request.user
        if request.method == 'GET':
            if not SalesMan.objects.filter(salesmanuser__user=user).exists():
                sales_man = SalesMan.objects.all().values('id', 'name', 'email', 'qr_code')
                res = None
                if sales_man.count():
                    rand_int = random.randint(1, len(sales_man))
                    res = sales_man[rand_int - 1]
            else:
                res = SalesMan.objects.filter(salesmanuser__user=user).values('id', 'name', 'email', 'qr_code')[0]
            return Response(res)
        else:
            data = request.data
            data['user'] = user
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': '操作成功'})


class UserInfoViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilterSet

    def list(self, request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            raise exceptions.PermissionDenied('非管理员无权限访问该接口')
        self.queryset = self.queryset.exclude(user__role='ADMIN')
        self.serializer_class = ListUserInfoSerializer
        return super().list(request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        if not self.queryset.filter(user=user).exists():
            raise exceptions.ValidationError('暂未找到该用户的用户信息。')
        instance = self.queryset.get(user=user)
        return instance

    @detail_route(methods=['GET', 'PUT', 'PATCH'],
                  serializer_class=PersonalFIleUserInfoSerializer)
    def personal_file(self, request, pk):
        instance = self.get_object()
        if request.method != 'GET':
            partial = True if request.method == 'PATCH' else False
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            instance = self.get_object()
        return Response(self.get_serializer(instance).data)


class UserScoreDetailViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = UserScoreDetail.objects.all()
    serializer_class = UserScoreDetailSerializer

    def get_object(self):
        user = self.request.user
        if not self.queryset.filter(user=user).exists():
            raise exceptions.ValidationError('暂未找到该用户的成绩单详情，请先创建。')
        instance = self.queryset.get(user=user)
        return instance
