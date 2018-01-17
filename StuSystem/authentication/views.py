# coding: utf-8

from authentication.functions import auto_assign_sales_man
from authentication.serializers import UserSerializer, LoginSerializer, CreateAccountSerializer, \
    UserInfoSerializer, PersonalFIleUserInfoSerializer, StudentScoreDetailSerializer, SalesManUserSerializer, \
    AssignSalesManSerializer, ClientAuthorizeSerializer, CustomUserInfoSerializer
from coupon.models import Coupon
from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from micro_service.service import AuthorizeServer, WeixinServer
from authentication.models import User, UserInfo, StudentScoreDetail
from micro_service.wx_smart_functions import WxSmartProgram


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

    @list_route(['GET'], serializer_class=ClientAuthorizeSerializer)
    def authorize(self, request):
        """客户端登录获取授权"""
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        res = WxSmartProgram.code_authorize(code)
        response = Response(res)
        response.set_cookie('ticket', res['ticket'])
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
        if all([user_info.name, user_info.email, user_info.wechat, user_info.wcampus]) is False:
            need_complete_stu_info = True
        else:
            need_complete_stu_info = False
        return Response({
            'need_complete_stu_info': need_complete_stu_info,
            'user_id': user.id,
            "valid_sales_man": True if user_info.valid_sales_man else False
        })

    @list_route(['put'])
    def logout(self, request):
        """ 退出登录
        """
        ticket = request.COOKIES.get('ticket')
        AuthorizeServer.delete_ticket(ticket)
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
        res = Coupon.objects.filter(usercoupon__user=user, usercoupon__status="TO_USE").values(
            'id', 'coupon_code', 'amount', 'info', 'start_time', 'end_time')
        return Response(res)

    @detail_route(['GET', 'POST'], serializer_class=SalesManUserSerializer)
    def sales_man(self, request, pk):
        """
        获取销售人员信息
        """
        user = request.user
        if request.method == 'GET':
            res = auto_assign_sales_man(user)
            return Response(res)
        else:
            data = request.data
            data['user'] = user
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': '操作成功'})

    @list_route()
    def sharing_qrcode(self, request):
        """用户分享自己的二维码"""
        user = request.user
        valid_time = 2*60*60
        qr_img_url = WeixinServer.get_temporary_qr_code(action_name='QR_STR_SCENE',
                                                        scene_id='recommend_user_id_%s' % user.id,
                                                        expired_time=valid_time)
        return Response({'qr_img_url': qr_img_url})

    @list_route(serializer_class=AssignSalesManSerializer)
    def assign_sales_man(self, request):
        data = self.request.query_params
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()
        ticket = res.get('ticket')
        response = Response(res.get('sales_man'))
        response.set_cookie('ticket', ticket)
        return response


class UserInfoViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        user = self.request.user
        if not self.queryset.filter(user=user).exists():
            raise exceptions.ValidationError('暂未找到该用户的用户信息。')
        instance = self.queryset.get(user=user)
        return instance

    @detail_route(['PUT', 'PATCH'], serializer_class=CustomUserInfoSerializer)
    def user_info(self, request, pk):
        # 兼容微信小程序，提供更新用户信息接口
        partial = False if request.method == 'PUT' else True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.serializer_class(instance).data)

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

    @list_route(['GET'])
    def complete_personal_file(self, request):
        user = request.user
        instance = self.queryset.filter(user=user).first()
        if not instance:
            raise exceptions.ValidationError('无效的user')
        need_complete_personal_file = all([instance.first_name, instance.last_name, instance.gender, instance.id_number,
                                           instance.major, instance.graduate_year, instance.gpa])
        return Response({'need_complete_personal_file': True if not need_complete_personal_file else False})


class StudentScoreDetailViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """成绩单寄送地址视图"""
    queryset = StudentScoreDetail.objects.filter(is_active=True)
    serializer_class = StudentScoreDetailSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()