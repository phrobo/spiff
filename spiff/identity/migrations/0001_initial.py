# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('required', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_view_private_fields', 'Can view private fields'), ('can_edit_protected_fields', 'Can edit protected fields')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('field', models.ForeignKey(to='identity.Field')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagline', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lastSeen', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False)),
                ('displayName', models.TextField()),
                ('fields', models.ManyToManyField(to='identity.Field', through='identity.FieldValue')),
                ('user', models.OneToOneField(related_name=b'identity', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_view_hidden_identities', 'Can view hidden identities'), ('list_identities', 'Can list identities')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserResetToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name=b'resetTokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='identity',
            field=models.ForeignKey(related_name=b'attributes', to='identity.Identity'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='AuthenticatedUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='AuthenticatedUserGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.group',),
        ),
    ]
