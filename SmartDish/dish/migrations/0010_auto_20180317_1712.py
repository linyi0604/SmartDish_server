# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0009_auto_20180301_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishGrade',
            field=models.FloatField(default=0.0, verbose_name='评分'),
        ),
        migrations.AlterField(
            model_name='dishinfo',
            name='dishSellCount',
            field=models.IntegerField(default=0, verbose_name='销量'),
        ),
    ]
