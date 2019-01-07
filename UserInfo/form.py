from django import forms
from django.contrib.auth.models import User


# 注册表单
class RegisterForm(forms.Form):

    username = forms.CharField(
        # min_length=5,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'text',
                'placeholder': 'User Name',
            }
        ),
    )
    email = forms.EmailField(
        # min_length=5,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'type': 'text',
                'class': 'text',
                'placeholder': '你的邮箱',
            }
        ),
    )
    password1 = forms.CharField(
        # min_length=5,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'id': 'pwd1',
                'type': 'password',
                'class': 'text',
                'placeholder': '输入密码',
            }
        )
    )
    password2 = forms.CharField(
        # min_length=5,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'id': 'pwd2',
                'type': 'password',
                'class': 'text',
                'placeholder': '确认密码',
                'onkeyup': "validate()",
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('用户名至少3个字符啊')
        elif len(username) > 16:
            raise forms.ValidationError('用户名太长惹，不能超过16个字符啊')
        else:
            exist_name = User.objects.filter(username__exact=username)
            if len(exist_name) > 0:
                raise forms.ValidationError('这个名字被占用啦')
        return username

    def clean_email(self):

        email = self.cleaned_data.get('email')
        if len(email) < 5:
            raise forms.ValidationError('邮箱有点短啊')
        elif len(email) > 254:
            raise forms.ValidationError('邮箱太长了吧')
        else:
            exist_email = User.objects.filter(email__exact=email)
            if len(exist_email) > 0:
                raise forms.ValidationError('这个邮箱已经被使用啦')
        return email

    def clean_password1(self):

        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('密码要超过6位啊')
        elif len(password1) > 20:
            raise forms.ValidationError('密码太长了')
        return password1

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('密码不一致')
        return password2


# 登录表单
class LoginForm(forms.Form):

    username = forms.CharField(
        min_length=5,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-username form-control',
                'id':"form-username",
                'placeholder': "Username...",
                'name':'form-username',
            }
        ),
        error_messages={
            'required': '用户名不能为空'
        }
    )
    password = forms.CharField(
        min_length=5,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'name': 'form-password',
                'placeholder': 'Password...',
                'class': 'form-password form-control',
                'id': 'form-password',
            }
        )
    )
