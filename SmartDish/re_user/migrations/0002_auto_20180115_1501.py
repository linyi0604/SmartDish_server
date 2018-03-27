# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuserinfo',
            name='detail',
            field=models.CharField(verbose_name='餐厅介绍', max_length=1000),
        ),
        migrations.AlterField(
            model_name='reuserinfo',
            name='name',
            field=models.CharField(verbose_name='餐厅名称', max_length=100),
        ),
    ]
