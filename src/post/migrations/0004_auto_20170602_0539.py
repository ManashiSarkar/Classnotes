# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 05:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='recepient',
            new_name='recipient',
        ),
    ]
