# coding: utf-8
from rest_framework.routers import SimpleRouter

from source.views import ProjectViewSet, CampusViewSet, CourseViewSet, UserCourseViewSet, CourseProjectViewSet

router = SimpleRouter()

router.register('project', ProjectViewSet)
router.register('campus', CampusViewSet)
router.register('course', CourseViewSet)
router.register('course_project', CourseProjectViewSet)
router.register('user_course', UserCourseViewSet)
urlpatterns = router.urls