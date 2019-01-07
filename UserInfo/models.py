from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# 拓展user表
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    usericon = models.ImageField(verbose_name='用户头像', max_length=100, upload_to='headimages/',
                                 default='/headimages/default.jpg', null=True)
    description = models.CharField(verbose_name='个人说明', null=True, default='说明啊...', max_length=150)
    phone = models.CharField(verbose_name='手机号码', null=True, max_length=11)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()


# 邮箱验证模型
class EmailVerifyRecord(models.Model):

    Send_Type_Choice = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.CharField(max_length=254, verbose_name='邮箱')
    send_time = models.DateTimeField(default=now, verbose_name='发送时间')
    send_type = models.CharField(verbose_name='验证码类型', choices=Send_Type_Choice, max_length=15)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ('{0}({1})'.format(self.code, self.email))

