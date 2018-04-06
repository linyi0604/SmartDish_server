# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0013_auto_20180331_1433'),
        ('customer_user', '0004_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('isLogin', models.BooleanField(default=False, verbose_name='是否登陆用户')),
                ('username', models.CharField(default='', max_length=100, verbose_name='用户名')),
                ('customer', models.ForeignKey(default='', to='customer_user.CustomerUserInfo', verbose_name='顾客')),
                ('dish', models.ForeignKey(to='dish.DishInfo', verbose_name='菜品')),
            ],
            options={
                'db_table': 'customer_record',
            },
        ),
    ]
