# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from course.models import Project, Campus, CampusType, Course, UserCourse
from course.serializers import ProjectSerializer, CampusSerializer, CampusTypeSerializer, \
    CourseSerializer, CurrentCourseProjectSerializer, CreateUserCourseSerializer


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


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @list_route()
    def get_current_course_count(self, request):
        """获取当前已选课数量"""
        user = request.user
        serializer = CurrentCourseProjectSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        current_course_count = UserCourse.objects.filter(user=user, project_id=project).count()
        course_count = Project.objects.get(id=project).course_num
        return Response({'course_count': course_count, 'current_course_count': current_course_count})

    @list_route()
    def current_courses(self, request):
        """
        当前项目可选课程
        """
        serializer = CurrentCourseProjectSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        courses = self.queryset.filter(project_id=project)
        return Response(self.serializer_class(courses, many=True).data)

    @list_route(['POST'], serializer_class=CreateUserCourseSerializer)
    def create_user_course(self, request):
        """
        学生选课
        """
        data = request.data
        data['user'] = request.user
        serializer = CurrentCourseProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': '操作成功'})