# coding: utf-8
"""StuSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from utils import index

urlpatterns = [
    url(r'^admin/', include('admin.urls')),  # 设置模块
    url(r'^auth/', include('authentication.urls')),  # 登陆模块
    url(r'^common/', include('common.urls')),  # 通用模块
    url(r'^coupon/', include('coupon.urls')),  # 优惠券模块
    url(r'^source/', include('source.urls')),  # 课程模块
    url(r'^market/', include('market.urls')),  # 市场推广模块
    url(r'^order/', include('order.urls')),  # 订单模块
    url(r'^', index.view)  # index页面
]
