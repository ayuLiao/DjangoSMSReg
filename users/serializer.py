import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from SMSReg.settings import REGEX_MOBILE
from .models import VerifyCode,ImageCode

# 可直接获得用户
User = get_user_model()

# 继承最基本的Serializer
class SmsSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    # 这里使用了write_only是因为后面我们将code字段通过del方法删除了，所以在序列化时，不使用write_only字段会报错，
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text="验证码")
    # 图片验证码
    imagecode = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="图片验证码",
                                      error_messages={
                                          "blank": "请输入图片验证码",
                                          "required": "请输入图片验证码",
                                          "max_length": "图片验证码格式错误",
                                          "min_length": "图片验证码格式错误"
                                      }, help_text="图片验证码")
    imagecodeid = serializers.CharField(required=True, write_only=True, label='图片验证码ID')

    # UniqueValidator:验证数据集中数据的唯一性，用户不能重复注册
    username = serializers.CharField(label='手机号', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])

    password = serializers.CharField(style={'input_type':'password'}, label='密码', write_only=True)

    def create(self, validated_data):
        # 继承
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        # 加密密码
        user.set_password(validated_data['password'])
        user.save()
        return user


    def validate_imagecode(self,imagecode):
        # initial_data是没有经过serializers处理过的数据,post中需要传入imagecodeid
        image_code = ImageCode.objects.filter(codeid=self.initial_data['imagecodeid'])
        five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        timage_code = image_code.filter(add_time__gte=five_mintes_ago)
        if not timage_code:
            raise serializers.ValidationError("图片验证码超时")
        if image_code:
            k = str(image_code[0])
            k2 = str(image_code[0]).lower()
            if str(image_code[0]).lower() != imagecode.lower():
                raise serializers.ValidationError("图片验证码错误")
        else:
            raise serializers.ValidationError("图片验证码错误")


    def validate_code(self, code):
        # post中需要传入username
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            # 5分钟有效期
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        '''
        对序列化的字段统一操作，删除不需要的验证存库的字段
        '''
        attrs['mobile'] = attrs['username']
        del attrs['code']
        del attrs['imagecode']
        del attrs['imagecodeid']
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password", 'imagecode', 'imagecodeid','name')
