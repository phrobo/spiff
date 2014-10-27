# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Federation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('lastContact', models.DateTimeField()),
                ('ttl', models.IntegerField()),
                ('enabled', models.BooleanField(default=True)),
                ('alias', models.TextField()),
                ('permissions', models.ManyToManyField(to='auth.Permission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
