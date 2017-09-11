# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 13:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ambiente', '0011_auto_20170901_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='responsavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Responsavel pela tarefa'),
        ),
    ]