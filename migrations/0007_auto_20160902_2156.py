# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-02 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0006_auto_20160902_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itunesgenre',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]