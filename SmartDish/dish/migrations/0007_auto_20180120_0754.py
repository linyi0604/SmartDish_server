# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0006_auto_20180120_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishFeature',
            field=models.CharField(max_length=100, verbose_name='特点id列表', default=''),
        ),
    ]
