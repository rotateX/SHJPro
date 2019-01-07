# Generated by Django 2.1.2 on 2018-10-05 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SHJ', '0002_auto_20181005_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'get_latest_by': 'put_time', 'ordering': ['-pub_time'], 'verbose_name': '作品', 'verbose_name_plural': '作品列表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': '类别名称', 'verbose_name_plural': '标签列表'},
        ),
    ]