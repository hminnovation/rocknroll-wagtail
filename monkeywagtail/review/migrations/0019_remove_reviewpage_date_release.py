# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-22 16:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0018_auto_20160922_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewpage',
            name='date_release',
        ),
    ]