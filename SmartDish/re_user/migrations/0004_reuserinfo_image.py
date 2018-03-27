# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0003_auto_20180118_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='reuserinfo',
            name='image',
            field=models.CharField(default='', verbose_name='图片路径', max_length=50),
        ),
    ]
