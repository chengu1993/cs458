# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cuisinelabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeID', models.IntegerField(verbose_name=b'place_id')),
                ('labelID', models.IntegerField(verbose_name=b'label_id')),
            ],
        ),
    ]
