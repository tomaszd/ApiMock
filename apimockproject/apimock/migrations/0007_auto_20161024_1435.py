# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apimock', '0006_auto_20161024_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockedapi',
            name='easily_updatable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mockedapi',
            name='Error_403',
            field=models.CharField(default=b'wrong used Data!', max_length=200),
        ),
    ]