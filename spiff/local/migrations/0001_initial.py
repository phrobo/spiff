# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logo', models.CharField(default=b'/logo.png', max_length=100)),
                ('openIcon', models.CharField(max_length=100, blank=True)),
                ('closedIcon', models.CharField(max_length=100, blank=True)),
                ('url', models.CharField(max_length=100, null=True, blank=True)),
                ('open', models.BooleanField(default=False)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=100, null=True, blank=True)),
                ('lastChange', models.DateTimeField(auto_now_add=True)),
                ('motd', models.TextField(blank=True)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpaceContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('space', models.ForeignKey(to='local.SpaceConfig')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpaceFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.TextField()),
                ('space', models.ForeignKey(to='local.SpaceConfig')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
