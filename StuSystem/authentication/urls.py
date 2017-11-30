# coding: utf-8
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserInfoViewSet, StudentScoreDetailViewSet

router = SimpleRouter()
router.register('user', UserViewSet)                            # 登录相关
router.register('user/info', UserInfoViewSet)                   # 用户信息
router.register('user/score_detail', StudentScoreDetailViewSet) # 成绩单寄送地址视图

urlpatterns = router.urls