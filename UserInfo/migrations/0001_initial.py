# Generated by Django 2.1 on 2018-12-11 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usericon', models.ImageField(default='/headimages/default.jpg', null=True, upload_to='headimages/', verbose_name='用户头像')),
                ('description', models.CharField(default='说明啊...', max_length=150, null=True, verbose_name='个人说明')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='手机号码')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
    ]