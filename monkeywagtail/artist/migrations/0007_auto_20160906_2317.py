# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-06 22:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_artist_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='artist_name',
            new_name='title',
        ),
    ]
