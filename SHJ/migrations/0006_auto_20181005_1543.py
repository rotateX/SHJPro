# Generated by Django 2.1.2 on 2018-10-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SHJ', '0005_auto_20181005_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='created_age',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='创建年代'),
        ),
    ]
