# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 10:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_hosting', '0014_auto_20161225_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ('upload_date',), 'verbose_name': '\u0417\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f', 'verbose_name_plural': '\u0417\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f'},
        ),
    ]