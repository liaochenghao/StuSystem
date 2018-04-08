# coding: utf-8
from admin.filters import UserInfoFilterSet, UserCourseFilterSet
from admin.models import PaymentAccountInfo
from admin.functions import order_auto_notice_message, course_auto_notice_message, confirm_auto_notice_message, \
    score_auto_notice_message, switch_auto_notice_message, change_student_status
from authentication.models import UserInfo, StudentScoreDetail, User
from permissions.base_permissions import BaseOperatePermission
from common.models import SalesMan, FirstLevel
from source.models import Campus, Course, CourseProject
from rest_framework import exceptions
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from admin.serializers import AdminPaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer, \
    UserInfoRemarkSerializer, ConfirmCourseSerializer, CourseScoreSerializer, StudentScoreDetailSerializer, \
    CampusOverViewSerializer, SalesManSerializer, AdminUserCourseSerializer, \
    AdminCourseCreditSwitchSerializer, ConfirmUserCourseSerializer, ChildUserSerializer, AdminCourseSerializer, \
    AdminCreateUserCourseSerializer, AdminUserCourseAddressSerializer, AdminOrderSerializer, FirstLevelSerializer, \
    AdminAvailableCoursesSerializer
from order.models import UserCourse, Order
import logging

logger = logging.getLogger('django')


class AccountInfoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """付款账号设置ViewSet"""
    queryset = PaymentAccountInfo.objects.all()
    serializer_class = AdminPaymentAccountInfoSerializer
    permission_classes = [BaseOperatePermission]


class UserInfoViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """用户信息ViewSet"""
    queryset = UserInfo.objects.all().exclude(user__role='ADMIN').order_by('-create_time')
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilterSet
    permission_classes = [BaseOperatePermission]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('many'):
            return UserInfoSerializer(*args, **kwargs)
        return RetrieveUserInfoSerializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.bind_sales_man:
            self.queryset = UserInfo.objects.filter(sales_man=user.bind_sales_man).exclude(user__role='ADMIN')
        else:
            self.queryset = UserInfo.objects.all().exclude(user__role='ADMIN')
        return self.queryset

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
        data['remark_by'] = request.user.id
        serializer = UserInfoRemarkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(UserInfoRemarkSerializer(instance).data)

    @detail_route()
    def scores(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        # change_student_status(user, 'AFTER_SCORE')
        return Response(CourseScoreSerializer(user_course, many=True).data)


class StudentScoreDetailViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """用户成绩邮寄视图"""
    queryset = StudentScoreDetail.objects.all()
    serializer_class = StudentScoreDetailSerializer
    permission_classes = [BaseOperatePermission]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=self.request.query_params.get('user'))
        except:
            raise exceptions.ValidationError('无效的user')
        self.queryset = self.queryset.filter(user=user)
        return super().list(request, *args, **kwargs)


class StatisticsViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [BaseOperatePermission]

    @list_route()
    def students_overview(self, request):
        # students_num = self.queryset.filter(user__role='STUDENT').count()
        # personal_file_num = self.queryset.filter(english_name__isnull=False,
        #                                          phone__isnull=False,
        #                                          gender__isnull=False,
        #                                          id_number__isnull=False,
        #                                          major__isnull=False,
        #                                          gpa__isnull=False).count()
        # students_applyed = len(set(
        #     Order.objects.filter(status__in=['TO_PAY', 'TO_CONFIRM', 'CONFIRMED', 'CONFIRM_FAILED']).values_list(
        #         'user_id', flat=True)))
        # students_payed = len(set(Order.objects.filter(status='CONFIRMED').values_list('user_id', flat=True)))
        # res = {
        #     'students_num': students_num,
        #     'personal_file_num': personal_file_num,
        #     'students_applyed': students_applyed,
        #     'students_payed': students_payed
        # }
        student_status = dict(UserInfo.STUDENT_STATUS)
        filter_year = request.query_params.get('year')
        query_set = UserInfo.objects.all()
        query_set = query_set if not filter_year else query_set.filter(create_time__year=filter_year)
        student_status_dict = []
        for key, value in student_status.items():
            student_status_dict.append({
                'key': key,
                'verbose': value,
                'number': query_set.filter(student_status=key).count()
            })
        data = [{'all_number': query_set.count(), 'data': student_status_dict}]
        return Response(data)

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
    serializer_class = SalesManSerializer
    permission_classes = [BaseOperatePermission]


class AdminUserOrderViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """学生成绩视图"""
    queryset = UserCourse.objects.all()
    serializer_class = AdminUserCourseSerializer
    filter_class = UserCourseFilterSet
    permission_classes = [BaseOperatePermission]

    def update(self, request, *args, **kwargs):
        instance = super().update(request, *args, **kwargs)
        score_auto_notice_message(instance.data.get('course'), instance.data.get('user_info'))
        user_queryset = UserCourse.objects.filter(user_id=instance.data.get('user_info')['user']).values_list(
            'score_grade')
        user_scores_status = all([score[0] for score in user_queryset])
        if user_scores_status:
            change_student_status(instance.data.get('user_info')['user'], 'AFTER_SCORE')
        return instance

    @list_route(['GET', 'PUT'])
    def confirm_course(self, request):
        if request.method == 'GET':
            user_id = self.request.query_params.get('user')
            try:
                user = User.objects.get(id=user_id)
            except:
                raise exceptions.ValidationError('无效的user')
            user_course = UserCourse.objects.filter(user=user)
            return Response(ConfirmCourseSerializer(user_course, many=True).data)
        else:
            serializer = ConfirmUserCourseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.queryset.filter(user=data['user'], course=data['course'],
                                 project=data['project'], order=data['order']).update(status=data['status'])
            instance = self.queryset.filter(user=data['user'], course=data['course'], order=data['order']).first()
            confirm_auto_notice_message(usercourse=instance, user=data['user'])
            course_not_all_pass = UserCourse.objects.filter(user=data['user']).exclude(status='PASS').exists()
            userinfo_status = UserInfo.objects.filter(user=data['user'],
                                                      student_status__in=['NEW', 'PERSONAL_FILE', 'ADDED_CC',
                                                                          'SUPPLY_ORDER',
                                                                          'PAYMENT_CONFIRM', 'TO_CHOOSE_COURSE',
                                                                          'PICKUP_COURSE',
                                                                          'TO_CONFIRMED'])
            if userinfo_status.exists() and not course_not_all_pass:
                change_student_status(data['user'].id, 'CONFIRMED_COURSE')
            # if userinfo_status.filter(student_status='CONFIRMED_COURSE').exists():
            #     change_student_status(data['user'].id, 'AFTER_SCORE')
            return Response(self.get_serializer(instance).data)


class AdminUserCourseCreditSwitchViewSet(mixins.ListModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         viewsets.GenericViewSet):
    """学生学分转换视图"""
    queryset = UserCourse.objects.filter(user__role='STUDENT')
    serializer_class = AdminCourseCreditSwitchSerializer
    permission_classes = [BaseOperatePermission]

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user')
        try:
            user_id = int(user_id)
        except:
            raise exceptions.ValidationError('请传入正确的user参数')
        return Response(self.serializer_class(self.queryset.filter(user_id=user_id), many=True).data)

    def update(self, request, *args, **kwargs):
        instance = super().update(request, *args, **kwargs)
        user_id_dict = UserCourse.objects.filter(id=kwargs.get('pk')).values_list('user_id').first()
        switch_auto_notice_message(instance.data.get('user_info'), instance.data.get('course'),
                                   instance.data.get('credit_switch_status'), )
        if not UserCourse.objects.filter(user_id=user_id_dict[0],
                                         credit_switch_status='PRE_POSTED').exists():
            change_student_status(user_id_dict[0], 'SWITCH_CREDIT')
        return instance


class AdminUserCourseAddressViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    """学生成绩单寄送地址"""
    queryset = StudentScoreDetail.objects.filter(user__role='STUDENT')
    serializer_class = AdminUserCourseAddressSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user')
        if not user_id:
            raise exceptions.ValidationError('user为必填参数')
        try:
            user_id = int(user_id)
        except ValueError:
            raise exceptions.ValidationError('user必须为int值')
        self.queryset = self.queryset.filter(user_id=user_id)
        return super().list(request, *args, **kwargs)


class ChildUserViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """子账号管理"""
    queryset = User.objects.exclude(role='STUDENT')
    serializer_class = ChildUserSerializer
    permission_classes = [BaseOperatePermission]

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


class AdminCourseViewSet(mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """管理员选课"""
    queryset = UserCourse.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [BaseOperatePermission]
    filter_fields = ['user']

    def destroy(self, request, *args, **kwargs):
        user_instance = UserCourse.objects.filter(id=kwargs.get('pk')).values('user_id').first()
        instance = super().destroy(request, *args, **kwargs)
        change_student_status(user_instance.get('user_id'), 'TO_CHOOSE_COURSE')
        return instance

    @list_route(['POST'], serializer_class=AdminCreateUserCourseSerializer)
    def create_user_course(self, request):
        """管理员为学生选课"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        course_auto_notice_message(serializer.instance)
        return Response({'msg': '选课成功'})

    @list_route(['GET'], serializer_class=AdminAvailableCoursesSerializer)
    def available_courses(self, request):
        """学生当前订单，当前项目可以选择的课程"""
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        order = data['order']
        project = data['project']
        current_course_ids = UserCourse.objects.filter(user=user, order=order,
                                                       project=project).values_list('course_id', flat=True)
        available_courses = [{
            'id': item.course.id,
            'name': item.course.name,
            'course_code': item.course.course_code
        } for item in CourseProject.objects.filter(project=project).exclude(
            course_id__in=current_course_ids)]
        return Response(available_courses)

    @list_route(serializer_class=AdminAvailableCoursesSerializer)
    def current_courses(self, request):
        """学生当前订单，当前项目已选课程"""
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        order = data['order']
        project = data['project']
        current_courses = [{
            'id': item.id,
            'project': project.id,
            'order': order.id,
            'course': {
                'id': item.course.id,
                'course_code': item.course.course_code,
                'name': item.course.name
            }
        } for item in self.queryset.filter(user=user, order=order, project=project)]
        return Response(current_courses)

    @list_route()
    def course_to_confirm_count(self, request):
        """用户上传凭证待审核数量"""
        count = UserCourse.objects.filter(status='TO_CONFIRM').count()
        return Response({'course_to_confirm_count': count})


class AdminOrderViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """管理员订单管理"""
    queryset = Order.objects.all().select_related('user').prefetch_related('orderchartrelation_set__chart',
                                                                           'usercourse_set')
    serializer_class = AdminOrderSerializer
    permission_classes = [BaseOperatePermission]
    filter_fields = ['currency', 'payment', 'status', 'user']

    def get_queryset(self):
        if self.request.query_params.get('pagination') and self.request.query_params.get(
                'pagination').upper() == 'FALSE':
            self.pagination_class = None
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        instance = super().update(request, *args, **kwargs)
        order_auto_notice_message(instance.data, instance.data.get('user'))
        return instance


class NavigationViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = FirstLevel.objects.order_by('rank')
    serializer_class = FirstLevelSerializer
    pagination_class = None
    permission_classes = [BaseOperatePermission]

    def get_queryset(self):
        queryset = self.queryset.filter(firstlevelrole__role=self.request.user.role)
        return queryset
