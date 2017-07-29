# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-28 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_notes_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=25)),
                ('country', models.CharField(blank=True, max_length=10)),
                ('province', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(blank=True, max_length=10)),
                ('area', models.CharField(blank=True, max_length=20)),
                ('last_time', models.DateTimeField(auto_now=True)),
                ('times', models.IntegerField(default=1)),
                ('mark', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=500)),
                ('mark_time', models.DateTimeField(auto_now=True)),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.IpInfo')),
            ],
        ),
    ]
