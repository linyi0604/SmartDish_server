# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0007_auto_20180120_0754'),
        ('customer_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('customer', models.ForeignKey(verbose_name='顾客', to='customer_user.CustomerUserInfo')),
                ('dish', models.ForeignKey(verbose_name='菜品', to='dish.DishInfo')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
