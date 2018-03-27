# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0003_auto_20180118_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('typename', models.CharField(verbose_name='菜品分类名称', max_length=40)),
                ('re_id', models.ForeignKey(to='re_user.ReUserInfo', verbose_name='餐厅用户id')),
            ],
            options={
                'db_table': 'restaurant_DishType',
            },
        ),
    ]
