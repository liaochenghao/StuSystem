# coding: utf-8
import datetime

from admin.filters import UserInfoFilterSet, UserCourseFilterSet
from admin.models import PaymentAccountInfo
from authentication.models import UserInfo, UserScoreDetail, User
from common.models import SalesMan
from course.models import Project, Campus, ProjectResult, Course
from rest_framework import exceptions
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from admin.serializers import PaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer, \
    UserInfoRemarkSerializer, ConfirmCourseSerializer, CourseScoreSerializer, UserScoreDetailSerializer, \
    AdminProjectSerializer, CampusOverViewSerializer, SalsesManSerializer, AdminUserCourseSerializer, \
    AdminProjectResultSerializer, AddUserCourseScoreSerializer, ConfirmUserCourseSerializer, ChildUserSerializer, \
    AdminCourseSerializer, AdminCreateUserCourseSerializer
from order.models import UserCourse, Order


class AccountInfoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = PaymentAccountInfo.objects.all()
    serializer_class = PaymentAccountInfoSerializer


class UserInfoViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilterSet

    def get_queryset(self):
        if self.request.user.role != 'ADMIN':
            raise exceptions.PermissionDenied('非管理员无权限访问该接口')
        queryset = self.queryset.exclude(user__role='ADMIN')
        return queryset

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('many'):
            return UserInfoSerializer(*args, **kwargs)
        return RetrieveUserInfoSerializer(*args, **kwargs)

    def get_object(self):
        # pk 传过来的是user_id，需要转换为user_info
        user_id = self.kwargs.get('pk')
        try:
            user_info = self.queryset.get(user=user_id)
        except UserInfo.DoesNotExist:
            raise exceptions.NotFound('未找到user_info实例')
        return user_info

    @detail_route(['POST'])
    def add_remark(self, request, pk):
        data = request.data
        data['user_info'] = self.get_object().id
        serializer = UserInfoRemarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(UserInfoRemarkSerializer(instance).data)

    @detail_route()
    def confirm_course(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        return Response(ConfirmCourseSerializer(user_course, many=True).data)

    @detail_route()
    def scores(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        return Response(CourseScoreSerializer(user_course, many=True).data)


class UserScoreDetailViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    queryset = UserScoreDetail.objects.all()
    serializer_class = UserScoreDetailSerializer

    def get_object(self):
        # pk 传过来的是user_id，需要转换为user_score_detail
        user_id = self.kwargs.get('pk')
        user_score_detail, created = self.queryset.get_or_create(user_id=int(user_id))
        return user_score_detail


class AdminProjectViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = AdminProjectSerializer


class StatisticsViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    @list_route()
    def students_overview(self, request):
        students_num = self.queryset.filter(user__role='STUDENT').count()
        personal_file_num = self.queryset.filter(first_name__isnull=False,
                                                 last_name__isnull=False,
                                                 phone__isnull=False,
                                                 gender__isnull=False,
                                                 id_number__isnull=False,
                                                 major__isnull=False,
                                                 gpa__isnull=False).count()
        students_applyed = len(set(Order.objects.all().values_list('user_id', flat=True)))
        students_payed = len(set(Order.objects.filter(status='CONFIRMED').values_list('user_id', flat=True)))
        res = {
            'students_num': students_num,
            'personal_file_num': personal_file_num,
            'students_applyed': students_applyed,
            'students_payed': students_payed
        }
        return Response(res)

    @list_route()
    def campus_overview(self, request):
        campus = Campus.objects.all()
        return Response(CampusOverViewSerializer(campus, many=True).data)


class SalesManViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = SalesMan.objects.all()
    serializer_class = SalsesManSerializer


class AdminUserOrderViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """学生成绩视图"""
    queryset = UserCourse.objects.all()
    serializer_class = AdminUserCourseSerializer
    filter_class = UserCourseFilterSet

    @list_route(['PUT'])
    def add_score(self, request):
        serializer = AddUserCourseScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.queryset.filter(user=data['user'], course=data['course'], order=data['order'])\
            .update(score=data['score'], score_grade=data['score_grade'], reporting_time=datetime.datetime.now())
        instance = self.queryset.filter(user=data['user'], course=data['course'], order=data['order']).first()
        return Response(self.get_serializer(instance).data)

    @list_route(['PUT'])
    def confirm_course(self, request):
        serializer = ConfirmUserCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.queryset.filter(user=data['user'], course=data['course'], order=data['order']) \
            .update(status=data['status'])
        instance = self.queryset.filter(user=data['user'], course=data['course'], order=data['order']).first()
        return Response(self.get_serializer(instance).data)


class AdminUserProjectResultViewSet(mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    viewsets.GenericViewSet):
    """学生学分转换视图"""
    queryset = ProjectResult.objects.all()
    serializer_class = AdminProjectResultSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound('未找到用户信息')
        project_result, created = self.queryset.get_or_create(user=user)
        return project_result


class ChildUserViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.exclude(role='STUDENT')
    serializer_class = ChildUserSerializer

    @detail_route(['PUT'])
    def update_password(self, request, pk):
        instance = self.get_object()
        password = request.data.get('password')
        if not password:
            raise exceptions.ValidationError('请传入正确的password')
        if not len(password) >= 6:
            raise exceptions.ValidationError('密码必须大于6位')
        instance.set_password(password)
        instance.save()
        return Response({'msg': '密码修改成功'})


class AdminCourseViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """管理员选课"""
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer

    @list_route(['POST'], serializer_class=AdminCreateUserCourseSerializer)
    def create_user_course(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': '选课成功'})

    @list_route()
    def course_to_confirm_count(self, request):
        """用户上传凭证待审核数量"""
        count = UserCourse.objects.filter(status='TO_CONFIRM').count()
        return Response({'course_to_confirm_count': count})

