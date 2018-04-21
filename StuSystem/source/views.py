# coding: utf-8
from datetime import datetime
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from StuSystem.settings import DOMAIN, MEDIA_URL
from admin.functions import change_student_status
from authentication.models import UserInfo
from permissions.base_permissions import StudentReadOnlyPermission
from source.models import Project, Campus, Course, CourseProject
from source.serializers import ProjectSerializer, CampusSerializer, \
    CourseSerializer, CommonImgUploadSerializer, CourseFilterElementsSerializer, CurrentProjectCoursesSerializer, \
    UpdateProjectCourseFeeSerializer, CourseProjectSerializer, UserCourseSerializer, StudentAvailableCoursesSerializer, \
    CourseConfirmSerializer
from order.models import Order, UserCourse, ShoppingChart


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    基础视图
    """
    queryset = None
    serializer_class = None

    def get_queryset(self):
        if self.request.query_params.get('pagination') and self.request.query_params.get(
                'pagination').upper() == 'FALSE':
            self.pagination_class = None
        return super().get_queryset()


class CampusViewSet(BaseViewSet):
    """
    校区视图
    """
    queryset = Campus.objects.all().filter(is_active=True)
    serializer_class = CampusSerializer
    permission_classes = [StudentReadOnlyPermission]

    @detail_route()
    def all_projects(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, context={'api_key': 'all_projects'})
        return Response(serializer.data)


class ProjectViewSet(BaseViewSet):
    """项目视图"""
    queryset = Project.objects.filter(is_active=True).select_related('campus'). \
        prefetch_related('courseproject_set', 'courseproject_set__course').order_by('id')
    serializer_class = ProjectSerializer
    filter_fields = ['campus']
    permission_classes = [StudentReadOnlyPermission]

    @detail_route()
    def available_courses(self, request, pk):
        """新建课程关联时允许关联的课程列表"""
        instance = self.get_object()
        related_course_ids = instance.courseproject_set.filter(project=instance).values_list('course_id', flat=True)
        courses = Course.objects.exclude(id__in=related_course_ids)
        return Response(CourseSerializer(courses, many=True).data)

    @detail_route(serializer_class=StudentAvailableCoursesSerializer)
    def student_available_courses(self, request, pk):
        """根据学生订单，项目获取允许选课列表"""
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data['order']
        instance = self.get_object()
        current_course_ids = UserCourse.objects.filter(user=request.user, project=instance, order=order
                                                       ).values_list('course_id', flat=True)
        related_course_ids = instance.courseproject_set.filter(project=instance).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=related_course_ids).exclude(id__in=current_course_ids)
        course_list = CourseSerializer(courses, many=True, context={'api_key': 'related_courses_info'}).data
        for course in course_list:
            count = UserCourse.objects.filter(course_id=course['id'], project=instance).count()
            course['choose_number'] = count
        return Response({
            'chart': ShoppingChart.objects.filter(orderchartrelation__order_id=order, project=pk).values('id').first(),
            'course_list': course_list
        })

    @detail_route()
    def related_courses_detail(self, request, pk):
        """项目关联课程详情"""
        serializer = self.serializer_class(instance=self.get_object(), context={'api_key': 'related_courses'})
        return Response(serializer.data)

    @detail_route()
    def related_courses_info(self, request, pk):
        """项目关联课程简介"""
        my_course = [item.course for item in CourseProject.objects.filter(project=self.get_object())]
        res = CourseSerializer(my_course, many=True).data
        return Response(res)

    @detail_route(['PUT'], serializer_class=UpdateProjectCourseFeeSerializer)
    def project_course_fee(self, request, pk):
        """项目课程费用"""
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_fees = serializer.validated_data['project_fees']
        serializer.save_project_course_fee(instance, project_fees)
        return Response(ProjectSerializer(instance=instance).data)

    @detail_route()
    def project_available_student(self, request, pk):
        project = Project.objects.filter(id=pk).values('campus__name', 'name').first()
        order_query = Order.objects.filter(orderchartrelation__chart__project_id=pk,
                                           status__in=['TO_PAY', 'TO_CONFIRM', 'CONFIRMED']).values_list('user_id',
                                                                                                         flat=True)
        filter_status = request.query_params.get('student_status')
        if filter_status == 'payed':
            order_query = order_query.filter(status='CONFIRMED')
        query_set = UserInfo.objects.filter(
            user_id__in=[user_id for user_id in order_query]).values('user_id', 'name',
                                                                     'wechat', 'email',
                                                                     'user__studentscoredetail__university',
                                                                     'sales_man',
                                                                     'student_status',
                                                                     'user__last_login')
        if filter_status == 'chose':
            course_query = UserCourse.objects.filter(project_id=pk).values_list('user_id', flat=True).distinct()
            query_set = query_set.filter(user_id__in=[user_id for user_id in course_query])
        try:
            page = int(request.query_params.get('page', 1))
        except:
            page = 1
        count = len(query_set)
        query_set = query_set[(page - 1) * 15:page * 15]
        for item in query_set:
            item['student_status'] = dict(UserInfo.STUDENT_STATUS).get(item.pop('student_status'))
            item['university'] = item.pop('user__studentscoredetail__university')
        data = {'count': count, 'project': project.get('campus__name') + '-' + project.get('name'), 'data': query_set}
        return Response(data)


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.filter(is_active=True).prefetch_related('courseproject_set', 'courseproject_set__project')
    serializer_class = CourseSerializer
    filter_fields = []
    permission_classes = [StudentReadOnlyPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project')
        if project:
            try:
                project = int(project)
                if project == 0:
                    return queryset
            except:
                raise exceptions.ValidationError('请传入正确的project参数')
            course_ids = CourseProject.objects.filter(project_id=project).values_list('course_id', flat=True)
            queryset = queryset.filter(id__in=course_ids)
        return queryset

    @detail_route()
    def available_projects(self, request, pk):
        """新建项目关联时允许操作的项目列表"""
        instance = self.get_object()
        available_projects_ids = instance.courseproject_set.filter(course=instance).values_list('project_id', flat=True)
        projects = Project.objects.exclude(id__in=available_projects_ids)
        return Response(ProjectSerializer(projects, many=True).data)

    @detail_route()
    def course_available_student(self, request, pk):
        project_id = request.query_params.get('project_id')
        filter_dict = {'course_id': pk, 'project_id': project_id} if project_id else {'course_id': pk}
        query_set = UserCourse.objects.filter(**filter_dict).values(
            'user__userinfo__name', 'user_id', 'user__userinfo__sales_man', 'user__userinfo__wechat', 'project__name',
            'project__campus__name', 'create_time')
        course_obj = Course.objects.filter(id=pk).values('name', 'max_num').first()
        data = {}
        for item in query_set:
            item['name'] = item.pop('user__userinfo__name')
            item['sales_man'] = item.pop('user__userinfo__sales_man')
            item['wechat'] = item.pop('user__userinfo__wechat')
            item['project'] = item.pop('project__campus__name') + '-' + item.pop('project__name')
        data['student_list'] = query_set
        data['course_name'] = course_obj.get('name')
        data['max_num'] = course_obj.get('max_num')
        data['choose_num'] = len(query_set)
        return Response(data)

    @detail_route()
    def related_projects(self, request, pk):
        """获取关联的项目"""
        serializer = self.serializer_class(instance=self.get_object(), context={'api_key': 'related_projects'})
        return Response(serializer.data)

    @list_route()
    def filter_elements(self, request):
        campus = Campus.objects.all()
        return Response(CourseFilterElementsSerializer(campus, many=True).data)


class CourseProjectViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """课程与项目关联"""
    queryset = CourseProject.objects.all()
    serializer_class = CourseProjectSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': '关联成功'})


class UserCourseViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """学生选课, 审课，学分转换视图"""
    queryset = UserCourse.objects.all().select_related('course')
    serializer_class = UserCourseSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': '选课成功'})

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CourseConfirmSerializer
        return super().retrieve(request, *args, **kwargs)

    @list_route()
    def current_courses_info(self, request):
        """获取当前已购买项目，选课数量,课程总数及课程信息"""
        res = self.course_info('current_courses_info')
        return Response(res)

    @list_route()
    def current_project_courses(self, request):
        """获取当前项目，选课数量,课程总数及课程详细信息"""
        serializer = CurrentProjectCoursesSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data['order']
        project = serializer.validated_data['project']
        current_course = UserCourse.objects.filter(
            order=order, user=self.request.user, project=project).values_list('id', flat=True)
        current_all_course = Course.objects.filter(
            courseproject__project=project, is_active=True).exclude(id__in=current_course). \
            values('id', 'course_code', 'name', 'credit')
        return Response(current_all_course)

    @list_route()
    def my_scores(self, request):
        """我的成绩"""
        res = self.common_handle(request, 'my_scores')
        return Response(res)

    @list_route(['PUT', 'GET'], serializer_class=CommonImgUploadSerializer)
    def student_confirm_course(self, request):
        """学生审课"""
        res = self.common_handle(request, 'student_confirm_course')
        if request.method == 'PUT':
            queruset = Order.objects.filter(user_id=request.user.id, status='CONFIRMED').values(
                'orderchartrelation__chart__course_num')
            choose_course = sum([order.get('orderchartrelation__chart__course_num') for order in queruset])
            if choose_course == UserCourse.objects.filter(user_id=request.user.id,
                                                          status='TO_CONFIRM').count():
                change_student_status(request.user.id, 'TO_CONFIRMED')
        return Response(res)

    @list_route(methods=['PUT', 'GET'], serializer_class=CommonImgUploadSerializer)
    def course_credit_switch(self, request):
        """学分转换证明"""
        res = self.common_handle(request, 'course_credit_switch')
        if request.method == 'PUT':
            if not UserCourse.objects.filter(user_id=request.user.id,
                                             credit_switch_status__in=['POSTED', 'PRE_POSTED']).exists():
                change_student_status(request.user.id, 'SWITCHED_COURSE')
        return Response(res)

    def common_handle(self, request, api_key):
        """学生审课，学分转换通用处理"""
        if request.method == 'GET':
            res = self.course_info(api_key)
        else:
            context = {'api_key': api_key, 'request': request}
            serializer = self.serializer_class(data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            user_course = UserCourse.objects.filter(user=request.user,
                                                    course=serializer.validated_data['course'],
                                                    order=serializer.validated_data['order'],
                                                    project=serializer.validated_data['project']).first()
            if user_course and api_key == 'course_credit_switch':
                user_course.switch_img = serializer.validated_data['switch_img']
                if serializer.validated_data.get('switch_remark'):
                    user_course.switch_remark = serializer.validated_data['switch_remark']
                user_course.credit_switch_status = 'SWITCHED'
            elif user_course and api_key == 'student_confirm_course':
                user_course.confirm_img = serializer.validated_data['confirm_img']
                if serializer.validated_data.get('confirm_remark'):
                    user_course.confirm_remark = serializer.validated_data['confirm_remark']
                user_course.status = 'TO_CONFIRM'
            user_course.save()
            res = {'msg': '图片上传成功'}
        return res

    def course_info(self, key=None):
        """
        已购买项目，选课数量,课程总数, 课程信息
        :return:
        """
        res = []
        payed_orders = Order.objects.filter(user=self.request.user, status='CONFIRMED')
        for order in payed_orders:
            charts = ShoppingChart.objects.filter(orderchartrelation__order=order,
                                                  orderchartrelation__order__status='CONFIRMED')
            for chart in charts:
                current_courses = UserCourse.objects.filter(user=self.request.user, order=order, project=chart.project,
                                                            course__courseproject__project=chart.project). \
                    values('course__id', 'course__course_code', 'course__name', 'course__courseproject__address',
                           'course__courseproject__start_time', 'course__courseproject__end_time',
                           'course__courseproject__professor', 'status', 'credit_switch_status', 'confirm_img',
                           'switch_img', 'score', 'score_grade', 'reporting_time', 'post_datetime', 'post_channel',
                           'post_number', 'id').order_by('-id')

                current_courses_list = []
                for item in current_courses:
                    current_course_item = {}
                    current_course_item.update(
                        {
                            'id': item.get('id'),
                            'course_id': item.get('course__id'),
                            'course_code': item.get('course__course_code'),
                            'name': item.get('course__name'),
                            'professor': item.get('course__courseproject__professor'),
                            'start_time': item.get('course__courseproject__start_time'),
                            'end_time': item.get('course__courseproject__end_time'),
                            'address': item.get('course__courseproject__address')
                        }
                    )
                    if key == 'student_confirm_course':
                        current_course_item.update({'status': {'key': item.get('status'),
                                                               'verbose': dict(UserCourse.STATUS).get(
                                                                   item.get('status'))},
                                                    'confirm_img': '%s%s%s' % (
                                                        DOMAIN, MEDIA_URL, item.get('confirm_img'))
                                                    if item.get('confirm_img') else None})
                    elif key == 'course_credit_switch':
                        current_course_item.update({'credit_switch_status': {'key': item.get('credit_switch_status'),
                                                                             'verbose': dict(
                                                                                 UserCourse.CREDIT_SWITCH_STATUS).get(
                                                                                 item.get('credit_switch_status'))
                                                                             },
                                                    'post_datetime': item.get('post_datetime'),
                                                    'post_channel': item.get('post_channel'),
                                                    'post_number': item.get('post_number'),
                                                    'switch_img': '%s%s%s' % (DOMAIN, MEDIA_URL, item.get('switch_img'))
                                                    if item.get('switch_img') else None})
                    elif key == 'my_scores':
                        current_course_item.update({
                            "score": item['score'],
                            "score_grade": item['score_grade'],
                            'reporting_time': item['reporting_time']
                        })
                    current_courses_list.append(current_course_item)

                if len(current_courses_list) == 0 and key != 'current_courses_info':
                    pass
                else:
                    current_course_num = len(current_courses)
                    res_item = {
                        'project': {
                            'id': chart.project.id,
                            'name': chart.project.campus.name + '-' + chart.project.name,
                            'start_time': chart.project.start_date,
                            'end_time': chart.project.end_date
                        },
                        'order': {
                            'id': order.id
                        },
                        'chart': chart.id,
                        'current_courses': current_courses_list
                    }
                    if key == 'current_courses_info':
                        res_item.update({
                            'course_num': chart.course_num,
                            'current_course_num': current_course_num
                        })
                    res.append(res_item)
        return res
