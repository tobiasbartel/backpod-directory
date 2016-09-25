# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-02 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_auto_20160902_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itunes',
            name='artist_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='itunes',
            name='collection_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='itunes',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='itunes',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]