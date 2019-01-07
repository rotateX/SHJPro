# coding=utf-8

from .models import *
from django.utils.timezone import now


def change_info(request):
    # 总访问量统计
    count_nums = TotalView.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = TotalView()
        count_nums.count = 1
    count_nums.save()
    # ip访问统计
    if 'HTTP_X_FORWARED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.META['REMOTE_ADDR']

    ip_exist = IpAddr.objects.filter(ip=str(client_ip))
    if ip_exist:
        ip_obj = ip_exist[0]
        ip_obj.count += 1
    else:
        ip_obj = IpAddr()
        ip_obj.ip = client_ip
        ip_obj.count = 1
    ip_obj.save()
    # 日访问统计
    date = now().date()
    today = DayView.objects.filter(view_time=date)
    if today:
        dv_obj = today[0]
        dv_obj.count += 1
    else:
        dv_obj = DayView()
        dv_obj.view_time = date
        dv_obj.count = 1
    dv_obj.save()



