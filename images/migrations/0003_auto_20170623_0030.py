# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20170623_0022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='user_like',
            new_name='users_like',
        ),
    ]
