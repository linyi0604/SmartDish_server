# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180317_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderno',
            name='商家是否查看过',
            field=models.BooleanField(default=False),
        ),
    ]
