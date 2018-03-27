# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderno',
            name='count',
            field=models.IntegerField(default=0, verbose_name='商品总数量'),
        ),
        migrations.AddField(
            model_name='orderno',
            name='price',
            field=models.FloatField(default=0, verbose_name='订单金额'),
        ),
    ]
