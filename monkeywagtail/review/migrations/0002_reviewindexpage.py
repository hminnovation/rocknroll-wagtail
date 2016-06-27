# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-26 20:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('listing_introduction', models.TextField(blank=True, help_text='Text to describe this section. Will appear on other pages that reference this feature section')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe this section. Will appear on the page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
