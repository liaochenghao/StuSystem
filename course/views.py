# coding: utf-8
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from course.models import Project, Campus, CampusType, Course, UserCourse, ProjectResult
from course.serializers import ProjectSerializer, MyProjectsSerializer, CampusSerializer, CampusTypeSerializer, \
    CourseSerializer, CurrentCourseProjectSerializer, CreateUserCourseSerializer, \
    MyCourseSerializer, MyScoreSerializer, ConfirmPhotoSerializer, GetProjectResultSerializer, UpdateImgSerializer


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
        projects = self.queryset.filter(order__user=request.user)
        data = self.serializer_class(projects, many=True, context={'user': request.user}).data
        return Response(data)

    @list_route(serializer_class=GetProjectResultSerializer)
    def project_result(self, request):
        projects = self.queryset.filter(order__user=request.user)
        data = self.serializer_class(projects, many=True, context={'user': request.user}).data
        return Response(data)

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

    @list_route(serializer_class=CurrentCourseProjectSerializer)
    def current_courses_info(self, request):
        """获取当前已选课数量和, 课程总数及课程信息"""
        user = request.user
        data = self.request.query_params.dict()
        data['user'] = user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        current_course_count = UserCourse.objects.filter(user=user, project_id=project).count()
        course_count = Project.objects.get(id=project).course_num
        courses = self.queryset.filter(project_id=project)
        data = CourseSerializer(courses, many=True).data
        res = {
            'course_count': course_count,
            'current_course_count': current_course_count,
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
        UserCourse.objects.filter(user=request.user,
                                  course=self.get_object()).update(confirm_photo=serializer.validated_data['confirm_photo'])
        return Response({'msg': '操作成功'})