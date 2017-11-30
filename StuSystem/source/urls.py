# coding: utf-8
from rest_framework.routers import SimpleRouter

from source.views import ProjectViewSet, CampusViewSet, CourseViewSet, UserCourseViewSet, CourseProjectViewSet

router = SimpleRouter()

router.register('project', ProjectViewSet)              # 项目相关
router.register('campus', CampusViewSet)                # 校区相关
router.register('course', CourseViewSet)                # 课程相关
router.register('course_project', CourseProjectViewSet) # 课程项目关联
router.register('user_course', UserCourseViewSet)       # 学生选课
urlpatterns = router.urls