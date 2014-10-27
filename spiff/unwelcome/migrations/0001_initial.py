# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnwelcomePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('reason', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('identity', models.ForeignKey(to='identity.Identity')),
                ('unwelsomePerson', models.ForeignKey(to='unwelcome.UnwelcomePerson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
