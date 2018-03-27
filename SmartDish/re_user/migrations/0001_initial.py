# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReUserInfo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(verbose_name='商家用户名', max_length=50)),
                ('password', models.CharField(verbose_name='密码', max_length=40)),
                ('name', models.CharField(verbose_name='餐厅名称', max_length=1000)),
                ('address', models.CharField(verbose_name='餐厅地址', max_length=100)),
                ('phone', models.CharField(verbose_name='餐厅电话', max_length=50)),
                ('detail', models.CharField(verbose_name='餐厅介绍', max_length=100)),
            ],
            options={
                'db_table': 'restaurant_info',
            },
        ),
    ]
