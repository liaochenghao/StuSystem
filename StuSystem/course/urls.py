# coding: utf-8
from rest_framework.routers import SimpleRouter

from course.views import ProjectViewSet, CampusViewSet, CourseViewSet

router = SimpleRouter()

router.register('project', ProjectViewSet)
router.register('campus', CampusViewSet)
router.register('', CourseViewSet)
urlpatterns = router.urls