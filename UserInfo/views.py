# coding=utf-8

from django.shortcuts import render
from django.contrib.auth.models import User
from UserInfo.models import UserProfile, EmailVerifyRecord
from UserInfo.form import RegisterForm, LoginForm
from UserInfo.sendmail import cf_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from SHJPro import settings


# 注册模块
def register(request):

    form = RegisterForm()
    return render(request, 'register.html', {
        'form': form
    })


# ajax提交注册信息
def AjaxReg(request):

    form = RegisterForm()
    res = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
            uer_profile = UserProfile(user=user)
            uer_profile.save()
            res['status'] = 'SUCCESS'
            cf_mail(email, 'register')
        else:
            res['status'] = 'ERROR'
            res['message'] = list(form.errors.values())
        return JsonResponse(res)
    return render(request, 'register.html', {
        'form': form
    })


# 激活用户
def user_active(request, active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    pass

# 登录模块
def login(request):
    pass
