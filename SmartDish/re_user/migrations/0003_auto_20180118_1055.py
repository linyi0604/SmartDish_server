# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('re_user', '0002_auto_20180115_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuserinfo',
            name='username',
            field=models.CharField(verbose_name='商家用户名', unique=True, max_length=50),
        ),
    ]
