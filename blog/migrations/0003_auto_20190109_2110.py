# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-09 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='article',
            name='last_edit',
            field=models.CharField(default='', max_length=32),
        ),
    ]
