# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0010_auto_20180317_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishDetail',
            field=models.CharField(verbose_name='菜品介绍', max_length=1000),
        ),
    ]
