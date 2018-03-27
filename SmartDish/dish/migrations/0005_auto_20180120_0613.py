# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0004_auto_20180119_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishFeature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('featureName', models.CharField(max_length=10, verbose_name='特征名称')),
            ],
            options={
                'db_table': 'dish_feature',
            },
        ),
        migrations.CreateModel(
            name='DishFeatureType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('typeName', models.CharField(unique=True, max_length=20, verbose_name='特征分类名称')),
            ],
            options={
                'db_table': 'dish_feature_type',
            },
        ),
        migrations.AddField(
            model_name='dishinfo',
            name='dishFeature',
            field=models.CharField(default='', max_length=100, verbose_name='特点id列表'),
        ),
        migrations.AddField(
            model_name='dishfeature',
            name='featureType',
            field=models.ForeignKey(to='dish.DishFeatureType', verbose_name='特征类别'),
        ),
    ]
