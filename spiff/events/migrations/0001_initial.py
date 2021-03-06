# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'permissions': (('can_reserve_resource', 'Can attach resources to events'),),
            },
            bases=(models.Model,),
        ),
    ]
