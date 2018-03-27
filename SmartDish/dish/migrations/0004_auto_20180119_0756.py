# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0003_auto_20180119_0630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dishtype',
            old_name='typename',
            new_name='typeName',
        ),
    ]
