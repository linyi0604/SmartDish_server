# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_user', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_payed',
            field=models.BooleanField(default=False, verbose_name='是否结帐'),
        ),
    ]
