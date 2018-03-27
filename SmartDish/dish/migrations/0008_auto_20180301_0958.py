# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0007_auto_20180120_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishinfo',
            name='dishPrice',
            field=models.FloatField(default=0.0, verbose_name='菜品价格'),
        ),
    ]
