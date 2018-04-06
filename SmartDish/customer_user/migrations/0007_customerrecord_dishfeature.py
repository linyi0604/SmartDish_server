# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_user', '0006_auto_20180405_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrecord',
            name='dishFeature',
            field=models.CharField(default='', max_length=500, verbose_name='特点id列表'),
        ),
    ]
