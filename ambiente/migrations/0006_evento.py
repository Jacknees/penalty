# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 10:46
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ambiente', '0005_auto_20170825_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.CharField(max_length=100, null=True, verbose_name='Descrição')),
                ('data_inicio', models.DateField(default=datetime.date.today)),
                ('data_fim', models.DateField(verbose_name='Data de término')),
                ('dia_evento', models.DateField(default=datetime.date.today)),
                ('id_agrupador', models.IntegerField()),
                ('quantidade_intervalos_repeticao', models.IntegerField(verbose_name='Se repete em')),
                ('intervalo', models.CharField(choices=[('D', 'Dias'), ('S', 'Semanas'), ('M', 'Meses')], max_length=1)),
                ('solicitacao_de_validacao', models.BooleanField(default=False)),
                ('momento_da_solicitacao', models.DateTimeField()),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criador')),
            ],
        ),
    ]
