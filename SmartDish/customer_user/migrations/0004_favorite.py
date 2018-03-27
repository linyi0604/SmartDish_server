# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0007_auto_20180120_0754'),
        ('customer_user', '0003_cart_is_payed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(verbose_name='顾客', to='customer_user.CustomerUserInfo')),
                ('dish', models.ForeignKey(verbose_name='菜品', to='dish.DishInfo')),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
    ]
