# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerUserInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(verbose_name='顾客用户名', unique=True, max_length=50)),
                ('password', models.CharField(verbose_name='密码', max_length=40)),
                ('name', models.CharField(verbose_name='客户昵称 姓名', max_length=100)),
                ('phone', models.CharField(verbose_name='电话号码', max_length=50)),
                ('detail', models.CharField(verbose_name='自我介绍', max_length=1000)),
            ],
            options={
                'db_table': 'customer_info',
            },
        ),
    ]
