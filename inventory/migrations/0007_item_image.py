# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-15 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20170215_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=b''),
        ),
    ]
