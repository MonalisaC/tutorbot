# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-06 06:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=5000)),
                ('detail', models.CharField(max_length=5000)),
                ('source', models.CharField(max_length=200)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('learned', models.BooleanField(default=False)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorbot.Answer')),
            ],
        ),
    ]
