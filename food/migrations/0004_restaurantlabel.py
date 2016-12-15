# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_extrainfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeID', models.IntegerField(verbose_name=b'place_id')),
                ('latitude', models.FloatField(verbose_name=b'latitude')),
                ('longitude', models.FloatField(verbose_name=b'longitude')),
                ('alcohol', models.IntegerField(verbose_name=b'alcohol')),
                ('smoking_area', models.IntegerField(verbose_name=b'smoking_area')),
                ('dress_code', models.IntegerField(verbose_name=b'dress_code')),
                ('accessibility', models.IntegerField(verbose_name=b'accessibility')),
                ('price', models.IntegerField(verbose_name=b'price')),
                ('Rambience', models.IntegerField(verbose_name=b'Rambience')),
                ('franchise', models.IntegerField(verbose_name=b'franchise')),
                ('area', models.IntegerField(verbose_name=b'area')),
                ('cuisine', models.IntegerField(verbose_name=b'cuisine')),
                ('parking_lot', models.IntegerField(verbose_name=b'parking_lot')),
            ],
        ),
    ]
