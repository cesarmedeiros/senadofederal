# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senadores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='codigo',
            field=models.CharField(default='', max_length=6, verbose_name='Código do Partido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partido',
            name='data_criacao',
            field=models.DateField(null=True, verbose_name='Data de Criação'),
        ),
    ]
