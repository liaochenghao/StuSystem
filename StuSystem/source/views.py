# coding: utf-8

from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from StuSystem.settings import DOMAIN, MEDIA_URL
from permissions.base_permissions import StudentReadOnlyPermission
from source.models import Project, Campus, Course, CourseProject
from source.serializers import ProjectSerializer, CampusSerializer, \
    CourseSerializer, MyScoreSerializer, CommonImgUploadSerializer, CourseFilterElementsSerializer, \
    UpdateProjectCourseFeeSerializer, CourseProjectSerializer, UserCourseSerializer
from order.models import Order, UserCourse, ShoppingChart, OrderChartRelation


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


class CampusViewSet(BaseViewSet):
    """
    校区视图
    """
    queryset = Campus.objects.filter(is_active=True)
    serializer_class = CampusSerializer
    permission_classes = [StudentReadOnlyPermission]

    @detail_route()
    def all_projects(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, context={'api_key': 'all_projects'})
        return Response(serializer.data)


class ProjectViewSet(BaseViewSet):
    """项目视图"""
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    permission_classes = [StudentReadOnlyPermission]

    def get_queryset(self):
        if self.request.query_params.get('pagination') and self.request.query_params.get('pagination').upper() == 'FALSE':
            self.pagination_class = None
        return super().get_queryset()

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


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [StudentReadOnlyPermission]

    def get_queryset(self):
        if self.request.query_params.get('pagination') and self.request.query_params.get('pagination').upper() == 'FALSE':
            self.pagination_class = None
        return super().get_queryset()

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
                        viewsets.GenericViewSet):
    """学生选课"""
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': '选课成功'})

    @list_route()
    def current_courses_info(self, request):
        """获取当前已购买项目，选课数量,课程总数及课程信息"""
        res = self.course_info('current_courses_info')
        return Response(res)

    @list_route()
    def my_scores(self, request):
        """我的成绩"""
        res = self.common_handle(request, 'my_scores')
        return Response(res)

    @list_route(['PUT', 'GET'], serializer_class=CommonImgUploadSerializer)
    def student_confirm_course(self, request):
        """学生审课"""
        res = self.common_handle(request, 'student_confirm_course')
        return Response(res)

    @list_route(methods=['PUT', 'GET'], serializer_class=CommonImgUploadSerializer)
    def course_credit_switch(self, request):
        """学分转换证明"""
        res = self.common_handle(request, 'course_credit_switch')
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
            if not user_course:
                raise exceptions.ValidationError('出入参数有误')
            if user_course and api_key == 'course_credit_switch':
                user_course.switch_img = serializer.validated_data['switch_img']
                user_course.credit_switch_status = 'SUCCESS'
            elif user_course and api_key == 'student_confirm_course':
                user_course.confirm_img = serializer.validated_data['confirm_img']
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
        chart_ids = OrderChartRelation.objects.filter(order__user=self.request.user, order__status='CONFIRMED').\
            values_list('chart', flat=True)
        payed_orders = Order.objects.filter(user=self.request.user, status='CONFIRMED')
        for order in payed_orders:
            charts = ShoppingChart.objects.filter(id__in=chart_ids)
            for chart in charts:
                current_courses = UserCourse.objects.filter(user=self.request.user, order=order, project=chart.project,
                                                            course__courseproject__project=chart.project). \
                    values('course__id', 'course__course_code', 'course__name', 'course__courseproject__address',
                           'course__courseproject__start_time', 'course__courseproject__end_time',
                           'course__courseproject__professor', 'status', 'credit_switch_status', 'confirm_img',
                           'switch_img', 'score', 'score_grade', 'reporting_time')

                current_courses_list = []
                for item in current_courses:
                    current_course_item = {}
                    current_course_item.update(
                        {
                            'id': item.get('course__id'),
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
                                                    'confirm_img': '%s%s%s' % (DOMAIN, MEDIA_URL, item.get('confirm_img'))
                                                    if item.get('confirm_img') else None})
                    elif key == 'course_credit_switch':
                        current_course_item.update({'credit_switch_status': {'key': item.get('credit_switch_status'),
                                                                             'verbose': dict(
                                                                                 UserCourse.CREDIT_SWITCH_STATUS).get(
                                                                                 item.get('credit_switch_status'))
                                                                             },
                                                    'switch_img': '%s%s%s' % (DOMAIN, MEDIA_URL, item.get('switch_img'))
                                                    if item.get('switch_img') else None})
                    elif key == 'my_scores':
                        current_course_item.update({
                            "score": item['score'],
                            "score_grade": item['score_grade'],
                            'reporting_time': item['reporting_time']
                        })
                    current_courses_list.append(current_course_item)

                current_course_num = len(current_courses)
                res_item = {
                    'project': {
                        'id': chart.project.id,
                        'name': chart.project.name
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