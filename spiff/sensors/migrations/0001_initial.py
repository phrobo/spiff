# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(0, b'http'), (1, b'exec'), (2, b'python'), (3, b'script')])),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(0, b'number'), (1, b'string'), (2, b'binary'), (3, b'json'), (4, b'temp'), (5, b'boolean')])),
                ('ttl', models.IntegerField(default=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(related_name=b'values', to='sensors.Sensor')),
            ],
            options={
                'ordering': ['-stamp'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='action',
            name='sensor',
            field=models.ForeignKey(related_name=b'actions', to='sensors.Sensor'),
            preserve_default=True,
        ),
    ]
