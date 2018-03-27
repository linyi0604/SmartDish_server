# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0004_reuserinfo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='reuserinfo',
            name='grade',
            field=models.FloatField(verbose_name='评分', default=0.0),
        ),
        migrations.AddField(
            model_name='reuserinfo',
            name='sellCount',
            field=models.IntegerField(verbose_name='销量', default=0),
        ),
    ]
