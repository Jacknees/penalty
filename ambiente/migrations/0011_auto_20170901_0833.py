# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 11:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ambiente', '0010_auto_20170830_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='ambiente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ambiente.Ambiente', verbose_name='Ambiente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evento',
            name='criador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criador'),
        ),
    ]