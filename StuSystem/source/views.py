# coding: utf-8
import json
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from StuSystem.settings import DOMAIN, MEDIA_URL
from source.models import Project, Campus, Course, CourseProject
from source.serializers import ProjectSerializer, CampusSerializer, \
    CourseSerializer, MyScoreSerializer, ConfirmPhotoSerializer, GetCourseCreditSwitchSerializer, \
    UpdateImgSerializer, ProjectMyScoreSerializer, CourseFilterElementsSerializer, UpdateProjectCourseFeeSerializer, \
    CourseProjectSerializer, UserCourseSerializer
from order.models import Order, UserCourse, CourseCreditSwitch, ShoppingChart


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

    @detail_route()
    def all_projects(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, context={'api_key': 'all_projects'})
        return Response(serializer.data)


class ProjectViewSet(BaseViewSet):
    """项目视图"""
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.query_params.get('pagination') and self.request.query_params.get('pagination').upper() == 'FALSE':
            self.pagination_class = None
        return super().get_queryset()

    @detail_route()
    def related_courses(self, request, pk):
        """所有项目关联的课程"""
        serializer = self.serializer_class(instance=self.get_object(), context={'api_key': 'related_courses'})
        return Response(serializer.data)

    @detail_route()
    def my_course(self, request, pk):
        """单个项目关联课程"""
        my_course = [item.course for item in CourseProject.objects.filter(project=self.get_object())]
        res = CourseSerializer(my_course, many=True).data
        return Response(res)

    @list_route(serializer_class=GetCourseCreditSwitchSerializer)
    def project_result(self, request):
        projects = self.queryset.filter(order__user=request.user, order__status='CONFIRMED')
        data = self.serializer_class(projects, many=True, context={'user': request.user}).data
        return Response(data)

    @list_route(serializer_class=ProjectMyScoreSerializer)
    def my_scores(self, request):
        user = request.user
        projects = self.queryset.filter(usercourse__user=user).distinct()
        serializer = self.serializer_class(projects, many=True, context={'user': user})
        return Response(serializer.data)

    @detail_route(methods=['PUT'], serializer_class=UpdateImgSerializer)
    def upload_img(self, request, pk):
        instance = self.get_object()
        if instance.img:
            raise exceptions.ValidationError('学分转换结果证明已经上传了')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate_project_result(instance, request.user)
        CourseCreditSwitch.objects.filter(project=instance, user=request.user).update(img=serializer.validated_data['img'])
        return Response({'msg': '图片上传成功'})

    @detail_route(['PUT'], serializer_class=UpdateProjectCourseFeeSerializer)
    def project_course_fee(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_fees = serializer.validated_data['project_fees']
        serializer.save_project_course_fee(instance, project_fees)
        return Response(ProjectSerializer(instance=instance).data)


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer

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
        res = self.course_info()
        return Response(res)

    @list_route(serializer_class=MyScoreSerializer)
    def my_scores(self, request):
        """我的成绩"""
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)
        data = self.serializer_class(user_courses, many=True).data
        return Response(data)

    @list_route(['PUT', 'GET'], serializer_class=ConfirmPhotoSerializer)
    def student_confirm_course(self, request):
        """学生审课"""
        if request.method == 'GET':
            res = self.course_info()
            return Response(res)
        else:
            # 上传审课图片
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_course = UserCourse.objects.filter(user=request.user,
                                                    course=serializer.validated_data['course'],
                                                    order=serializer.validated_data['order'],
                                                    project=serializer.validated_data['project']).first()
            if user_course:
                user_course.confirm_photo = serializer.validated_data['confirm_photo']
                user_course.status = 'TO_CONFIRM'
                user_course.save()
            return Response({'msg': '操作成功'})

    def course_info(self):
        """
        已购买项目，选课数量,课程总数, 课程信息
        :return:
        """
        res = []
        payed_orders = Order.objects.filter(user=self.request.user, status='CONFIRMED')
        for order in payed_orders:
            charts = ShoppingChart.objects.filter(id__in=json.loads(order.chart_ids))
            for chart in charts:
                current_courses = UserCourse.objects.filter(user=self.request.user, order=order, project=chart.project,
                                                            course__courseproject__project=chart.project). \
                    values('course__id', 'course__course_code', 'course__name', 'course__courseproject__address',
                           'course__courseproject__start_time', 'course__courseproject__end_time',
                           'course__courseproject__professor')
                current_courses = [{
                    'id': item.get('course__id'),
                    'course_code': item.get('course__course_code'),
                    'name': item.get('course__name'),
                    'professor': item.get('course__courseproject__professor'),
                    'start_time': item.get('course__courseproject__start_time'),
                    'end_time': item.get('course__courseproject__end_time'),
                    'address': item.get('course__courseproject__address')
                } for item in current_courses]
                current_course_num = len(current_courses)
                res.append({
                    'course_num': chart.course_num,
                    'current_course_num': current_course_num,
                    'project': {
                        'id': chart.project.id,
                        'name': chart.project.name
                    },
                    'order': {
                        'id': order.id
                    },
                    'chart_id': chart.id,
                    'current_courses': current_courses
                })
        return res