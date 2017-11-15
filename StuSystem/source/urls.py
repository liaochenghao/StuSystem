# coding: utf-8
from rest_framework.routers import SimpleRouter

from source.views import ProjectViewSet, CampusViewSet, CourseViewSet

router = SimpleRouter()

router.register('project', ProjectViewSet)
router.register('campus', CampusViewSet)
router.register('course', CourseViewSet)
urlpatterns = router.urls