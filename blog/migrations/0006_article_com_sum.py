# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-01-12 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_article_part_of'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='com_sum',
            field=models.IntegerField(default=0),
        ),
    ]