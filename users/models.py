from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    用户模块，继承Django默认的User，添加新字段
    """
    # null=True 数据库可空 blank=True HTML可空
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    # 手机号可以为空，本项目将username作为手机号来使用
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class ImageCode(models.Model):
    '''
    图片验证码，防止短信狂注册
    将随机生成的短信验证码图片和验证码ID返回前端，前端返回用户填写的结果和codeid
    '''
    codeid = models.CharField(max_length=40, verbose_name='验证码ID')
    code = models.CharField(max_length=10, verbose_name='验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "图片验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


