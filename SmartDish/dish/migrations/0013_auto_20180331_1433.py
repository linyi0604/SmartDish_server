# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0012_auto_20180331_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishFeature',
            field=models.CharField(verbose_name='特点id列表', max_length=500, default=''),
        ),
        migrations.AlterField(
            model_name='dishinfo',
            name='dishImage',
            field=models.CharField(max_length=100, verbose_name='图片路径'),
        ),
        migrations.AlterField(
            model_name='dishinfo',
            name='dishName',
            field=models.CharField(max_length=100, verbose_name='菜品名称'),
        ),
    ]
