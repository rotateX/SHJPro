from django.contrib import admin
from SiteView.models import DayView, TotalView, IpAddr

# Register your models here.


class DayViewAdmin(admin.ModelAdmin):
    list_display = ['view_time', 'count']


class TotalViewAdmin(admin.ModelAdmin):
    list_display = ['count']


class IpAddrAdmin(admin.ModelAdmin):
    list_display = ['ip', 'count']


admin.site.register(DayView, DayViewAdmin)
admin.site.register(TotalView, TotalViewAdmin)
admin.site.register(IpAddr, IpAddrAdmin)
