# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 16:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='images',
            new_name='image',
        ),
    ]