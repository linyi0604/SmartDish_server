# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0011_auto_20180331_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishDetail',
            field=models.CharField(max_length=5000, verbose_name='菜品介绍'),
        ),
    ]
