# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('identity', models.ForeignKey(related_name=b'certifications', to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old', models.TextField(null=True, blank=True)),
                ('new', models.TextField(null=True, blank=True)),
                ('property', models.TextField(null=True, blank=True)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('identity', models.ForeignKey(related_name=b'changes', to='identity.Identity')),
            ],
            options={
                'ordering': ['-stamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('type', models.IntegerField(choices=[(0, b'string'), (1, b'url'), (2, b'image')])),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('trainable', models.BooleanField(default=True)),
                ('certified_users', models.ManyToManyField(related_name=b'certified_resources', through='inventory.Certification', to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrainingLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.IntegerField()),
                ('identity', models.ForeignKey(related_name=b'trainings', to='identity.Identity')),
                ('resource', models.ForeignKey(related_name=b'trainings', to='inventory.Resource')),
            ],
            options={
                'ordering': ['-rank'],
                'permissions': (('can_train', 'Can update own training on resources'), ('certify', 'Can certify other users')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='users',
            field=models.ManyToManyField(to='identity.Identity', through='inventory.TrainingLevel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metadata',
            name='resource',
            field=models.ForeignKey(related_name=b'metadata', to='inventory.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='change',
            name='resource',
            field=models.ForeignKey(related_name=b'changelog', to='inventory.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='change',
            name='trained_identity',
            field=models.ForeignKey(related_name=b'training_changes', blank=True, to='identity.Identity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certification',
            name='resource',
            field=models.ForeignKey(related_name=b'certifications', to='inventory.Resource'),
            preserve_default=True,
        ),
    ]
