"""SMSReg URL Configuration

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
from django.conf.urls import url,include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from SMSReg.settings import MEDIA_ROOT
from users.views import UserViewset,SmsCodeViewset,ImageCodeView

router = DefaultRouter()
# 用户接口
router.register(r'users', UserViewset, base_name="users")
# 短信验证码接口
router.register(r'codes', SmsCodeViewset, base_name="codes")

urlpatterns = [
    url(r'^', include(router.urls)),
# 图片验证码
    url(r'^imagecode', ImageCodeView.as_view(), name='imagename'),
# 访问图片URL
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
