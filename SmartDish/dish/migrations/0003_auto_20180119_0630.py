# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_auto_20180118_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('dishName', models.CharField(verbose_name='菜品名称', max_length=40)),
                ('dishPrice', models.CharField(verbose_name='菜品价格', max_length=10)),
                ('dishImage', models.CharField(verbose_name='图片路径', max_length=50)),
                ('dishDetail', models.CharField(verbose_name='菜品介绍', max_length=500)),
            ],
            options={
                'db_table': 'dish_info',
            },
        ),
        migrations.AlterModelTable(
            name='dishtype',
            table='dish_type',
        ),
        migrations.AddField(
            model_name='dishinfo',
            name='dish_type',
            field=models.ForeignKey(verbose_name='菜品分类', to='dish.DishType'),
        ),
    ]
