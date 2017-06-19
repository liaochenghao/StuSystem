# coding: utf-8
from rest_framework.routers import SimpleRouter
from course.views import ProjectViewSet, CampusViewSet, CampusTypeViewSet, CourseViewSet

router = SimpleRouter()

router.register('project', ProjectViewSet)
router.register('campus', CampusViewSet)
router.register('campus_type', CampusTypeViewSet)
router.register('course', CourseViewSet)
urlpatterns = router.urls