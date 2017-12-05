# coding: utf-8
from rest_framework.routers import SimpleRouter

from admin.views import AccountInfoViewSet, UserInfoViewSet, StudentScoreDetailViewSet, \
    StatisticsViewSet, SalesManViewSet, AdminUserOrderViewSet, AdminUserCourseCreditSwitchViewSet, ChildUserViewSet, \
    AdminCourseViewSet, AdminOrderViewSet, NavigationViewSet, AdminUserCourseAddressViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)                             # 支付账号管理
router.register('user_info', UserInfoViewSet)                                   # 用户信息
router.register('student/score_info', StudentScoreDetailViewSet)                # 学生成绩单寄送地址
router.register('statistics', StatisticsViewSet)                                # 统计相关
router.register('sales_man', SalesManViewSet)                                   # 销售人员
router.register('user_course', AdminUserOrderViewSet)                           # 学生成绩
router.register('user_course_address', AdminUserCourseAddressViewSet)           # 成绩单寄送地址
router.register('course_credit_switch', AdminUserCourseCreditSwitchViewSet)     # 学分转换
router.register('child_user', ChildUserViewSet)                                 # 子账号
router.register('course', AdminCourseViewSet)                                   # 管理员为学生选课相关
router.register('order', AdminOrderViewSet)                                     # 订单相关
router.register('navigation', NavigationViewSet)                                # 导航项目

urlpatterns = router.urls