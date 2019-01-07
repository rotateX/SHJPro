import os
from django.core.mail import send_mail
from SHJPro import settings
from UserInfo.models import EmailVerifyRecord
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHJPro.settings')

# 生成随机字符
def random_str(randomlength=16):

    mail_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(randomlength):
        mail_str += random.choice(chars)
    return mail_str


# 发送邮件
def cf_mail(email, send_type="register"):

    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = "请点击下面的链接激活你的账号:http://192.168.1.233:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass

