# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_user', '0005_customerrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerrecord',
            name='username',
            field=models.CharField(max_length=200, verbose_name='用户名', default=''),
        ),
    ]
