# coding: utf-8
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from course.models import Project, Campus, CampusType, Course, ProjectResult
from order.models import UserCourse
from course.serializers import ProjectSerializer, MyProjectsSerializer, CampusSerializer, CampusTypeSerializer, \
    CourseSerializer, CurrentCourseProjectSerializer, CreateUserCourseSerializer, \
    MyCourseSerializer, MyScoreSerializer, ConfirmPhotoSerializer, GetProjectResultSerializer, UpdateImgSerializer, \
    ProjectMyScoreSerializer, CourseFilterElementsSerializer, CustomCampusTypeSerializer


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


class CampusTypeViewSet(BaseViewSet):
    """
    暑校类型视图
    """
    queryset = CampusType.objects.all()
    serializer_class = CampusTypeSerializer

    @list_route(serializer_class=CustomCampusTypeSerializer)
    def type_country_campus(self, request):
        """根据暑校类型，获取所在国家，获取所在校区"""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class CampusViewSet(BaseViewSet):
    """
    校区视图
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer

    @detail_route()
    def all_projects(self, request, pk):
        instance = self.get_object()
        all_projects = instance.project_set.all()
        return Response(ProjectSerializer(all_projects, many=True).data)


class ProjectViewSet(BaseViewSet):
    """项目视图"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @list_route(serializer_class=MyProjectsSerializer)
    def my_project(self, request):
        projects = self.queryset.filter(order__user=request.user).distinct()
        data = self.serializer_class(projects, many=True, context={'user': request.user}).data
        return Response(data)

    @detail_route()
    def my_course(self, request, pk):
        my_course = Course.objects.filter(project=self.get_object())
        res = CourseSerializer(my_course, many=True).data
        return Response(res)

    @list_route(serializer_class=GetProjectResultSerializer)
    def project_result(self, request):
        projects = self.queryset.filter(order__user=request.user)
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
        ProjectResult.objects.filter(project=instance, user=request.user).update(img=serializer.validated_data['img'])
        return Response({'msg': '图片上传成功'})


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_fields = ['project']

    @list_route(serializer_class=CurrentCourseProjectSerializer)
    def current_courses_info(self, request):
        """获取当前已选课数量和, 课程总数及课程信息"""
        user = request.user
        data = self.request.query_params.dict()
        data['user'] = user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        current_course_num = UserCourse.objects.filter(user=user, project_id=project).count()
        course_num = Project.objects.get(id=project).course_num
        courses = self.queryset.filter(project_id=project)
        data = CourseSerializer(courses, many=True).data
        res = {
            'course_num': course_num,
            'current_course_num': current_course_num,
            'course_info': data
        }
        return Response(res)

    @list_route(['POST'], serializer_class=CreateUserCourseSerializer)
    def create_user_courses(self, request):
        """
        学生选课
        """
        data = request.data
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': '操作成功'})

    @list_route(serializer_class=MyCourseSerializer)
    def my_courses(self, request):
        """我的课程表"""
        user = request.user
        data = self.serializer_class(Project.objects.filter(order__user=user, order__status='PAYED'), many=True,
                                     context={'user': user}).data
        return Response(data)

    @list_route(serializer_class=MyScoreSerializer)
    def my_scores(self, request):
        """我的成绩"""
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)
        data = self.serializer_class(user_courses, many=True).data
        return Response(data)

    @detail_route(['PUT'], serializer_class=ConfirmPhotoSerializer)
    def upload_confirm_photo(self, request, pk):
        """
        上传审课照片
        :param request:
        :param pk:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserCourse.objects.filter(user=request.user, course=self.get_object()).update(
            confirm_photo=serializer.validated_data['confirm_photo'], status='TO_CONFIRM')
        return Response({'msg': '操作成功'})

    @list_route()
    def filter_elements(self, request):
        campus = Campus.objects.all()
        return Response(CourseFilterElementsSerializer(campus, many=True).data)