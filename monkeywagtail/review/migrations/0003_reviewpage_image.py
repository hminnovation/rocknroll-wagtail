# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-26 23:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0013_make_rendition_upload_callable'),
        ('review', '0002_reviewindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Image to be used where this review is listed', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
