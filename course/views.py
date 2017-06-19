# coding: utf-8
from rest_framework import mixins, viewsets
from course.models import Project, Campus, CampusType
from course.serializers import ProjectSerializer, CampusSerializer, CampusTypeSerializer


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


class ProjectViewSet(BaseViewSet):
    """项目视图"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer