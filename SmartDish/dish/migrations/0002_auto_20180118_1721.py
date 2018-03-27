# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dishtype',
            old_name='re_id',
            new_name='re_user',
        ),
    ]
