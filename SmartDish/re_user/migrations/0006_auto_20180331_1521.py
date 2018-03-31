# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0005_auto_20180303_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuserinfo',
            name='image',
            field=models.CharField(verbose_name='图片路径', max_length=100, default=''),
        ),
    ]
