# coding: utf-8
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .models import User, UserInfo
from .functions import UserTicket
from .serializers import UserSerializer, LoginSerializer, CreateAccountSerializer, UserInfoSerializer


class UserViewSet(viewsets.GenericViewSet):
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

    @list_route(['POST'], serializer_class=CreateAccountSerializer)
    def check_account(self, request):
        # 检查账户信息
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.check_account(serializer.validated_data)
        return Response(res)

    @list_route()
    def logout(self, request):
        """ 退出登录
        """
        ticket = request.COOKIES.get('ticket')
        UserTicket.delete_ticket(ticket)
        ret_data = {'msg': '退出登录成功'}
        return Response(ret_data)


class UserInfoViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
