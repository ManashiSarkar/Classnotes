# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 18:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20170605_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 5, 18, 21, 37, 643018, tzinfo=utc)),
        ),
    ]