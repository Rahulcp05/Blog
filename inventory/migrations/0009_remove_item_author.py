# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-16 10:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_item_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='author',
        ),
    ]
