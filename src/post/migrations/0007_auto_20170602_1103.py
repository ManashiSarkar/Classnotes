# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 11:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20170602_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
