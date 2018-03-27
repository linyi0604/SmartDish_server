# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0008_auto_20180301_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishinfo',
            name='dishGrade',
            field=models.FloatField(default=0.0, verbose_name='月评分'),
        ),
        migrations.AddField(
            model_name='dishinfo',
            name='dishSellCount',
            field=models.IntegerField(default=0, verbose_name='月销量'),
        ),
    ]
