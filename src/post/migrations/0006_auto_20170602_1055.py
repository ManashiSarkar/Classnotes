# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20170602_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='read_time',
            field=models.DateTimeField(null=True),
        ),
    ]
