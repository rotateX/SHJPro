from .models import Comment
from django import forms

class CommentForm(forms.Form):

    name = forms.CharField(
        max_length=15,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'c_name',
                'placeholder': '昵称',
                # 'onfocus': "this.value=''",
                # 'onblur': "if (this.value == '') {this.value = 'Name';}",
            }
        ),
        error_messages = {
            'required': '请输入昵称',
            'max_length': '名字太长了！',
            'min_length': '名字至少三个字符！',
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'type': 'text',
                'id': 'c_email',
                'placeholder': '邮箱',
                # 'onfocus': "this.value=''",
                # 'onblur' : "if (this.value == '') {this.value = 'E-mail';}",
            }
        ),
        error_messages = {
            'invalid': '邮箱格式不正确',
            'required': '请输入有效邮箱',
        }
    )

    body = forms.CharField(
        max_length=250,
        min_length=5,
        widget=forms.Textarea(
            attrs={
                'id':'c_body',
                'cols': '77',
                'rows': '5',
                'placeholder': '内容',
                # 'onfocus': "this.value=''",
                # 'onblur': "if (this.value == '') {this.value = 'Message';}",
            }
        ),
        error_messages = {
            'required': '请输入内容',
            'max_length': '你说的太多了！',
        }
    )
