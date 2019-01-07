from django.db import models
from django.utils.timezone import now

# Create your models here.

class DayView(models.Model):
    view_time = models.DateField(verbose_name='日期', default=now,)
    count = models.IntegerField(verbose_name='访问次数', default=0)
    class Meta:
        verbose_name = '日访问统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.view_time)

# 总访问量
class TotalView(models.Model):
    count = models.IntegerField(verbose_name='访问总量', default=0)
    class Meta:
        verbose_name = '访问总量'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.count)

# ip地址和访问次数
class IpAddr(models.Model):
    ip = models.GenericIPAddressField(verbose_name='IP地址', max_length=64,)
    count = models.IntegerField(verbose_name='访问次数', default=0)
    class Meta:
        verbose_name = '用户IP'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.ip)
