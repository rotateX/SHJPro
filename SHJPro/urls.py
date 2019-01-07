"""SHJPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from SHJ import views as SHJ
from UserInfo import views as UserInfo

handler404 = SHJ.page_not_found
handler500 = SHJ.page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'mdeditor/', include('mdeditor.urls')), # mdeditor目录
    url(r'^$', SHJ.home, name='home'), # 都跳转到首页
    path('category/<str:id>', SHJ.category, name='category'),  # 按分类标签跳转
    path('post/<str:id>', SHJ.post, name='post'),  # 详情页跳转 需要文章id <str:id>
    path('getcomments/<str:id>', SHJ.get_comments, name='get_comments'),  # 评论提交
    path('favicon.ico', serve, {'path': 'static/images/favicon.ico'}),  # 处理找不到favicon.ico 问题
    url(r'^search/', include('haystack.urls')),
    path('register/', UserInfo.register, name='register'),  # 注册模块
    path('submit/', UserInfo.AjaxReg, name='AjaxReg'),
    path('siteinfo/', SHJ.date_echarts, name='date_echarts'),
    path('siteinfo/getdata/', SHJ.get_data, name='get_data' )
]

# 处理DEBUG = False 下找不到静态资源
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]


