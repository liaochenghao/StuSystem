# coding: utf-8
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework import exceptions
from .models import User, UserInfo, UserScoreDetail
from .functions import UserTicket
from .serializers import UserSerializer, LoginSerializer, CreateAccountSerializer, UserInfoSerializer, \
    PersonalFIleUserInfoSerializer, UserScoreDetailSerializer


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