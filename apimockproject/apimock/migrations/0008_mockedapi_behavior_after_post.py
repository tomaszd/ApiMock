# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apimock', '0007_auto_20161024_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockedapi',
            name='behavior_after_post',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
