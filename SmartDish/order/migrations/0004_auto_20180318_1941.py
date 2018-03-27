# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderno_商家是否查看过'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderno',
            name='商家是否查看过',
        ),
        migrations.AddField(
            model_name='orderno',
            name='is_checked',
            field=models.BooleanField(verbose_name='商家是否查看过', default=False),
        ),
    ]
