# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from course.models import Project, Campus, CampusType, Course
from course.serializers import ProjectSerializer, CampusSerializer, CampusTypeSerializer, CourseSerializer


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