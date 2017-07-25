# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 20:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0023_auto_20170718_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='topics',
            field=models.ManyToManyField(to='post.Topics'),
        ),
        migrations.AlterField(
            model_name='topics',
            name='topContributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
