# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20170605_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='user_type',
            field=models.CharField(default='green', max_length=30),
        ),
    ]
