# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_user', '0004_favorite'),
        ('dish', '0009_auto_20180301_1005'),
        ('re_user', '0005_auto_20180303_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(verbose_name='菜品数量', default=0)),
                ('dish', models.ForeignKey(verbose_name='菜品', to='dish.DishInfo')),
            ],
            options={
                'db_table': 'order_info',
            },
        ),
        migrations.CreateModel(
            name='OrderNo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_payed', models.BooleanField(verbose_name='是否结帐', default=False)),
                ('customer', models.ForeignKey(verbose_name='顾客', to='customer_user.CustomerUserInfo')),
                ('re_user', models.ForeignKey(verbose_name='餐厅', to='re_user.ReUserInfo')),
            ],
            options={
                'db_table': 'order_no',
            },
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='order',
            field=models.ForeignKey(verbose_name='订购单', to='order.OrderNo'),
        ),
    ]
