# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
        ('events', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name=b'events', to='identity.Identity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(related_name=b'owned_events', to='identity.Identity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='organizers',
            field=models.ManyToManyField(related_name=b'organized_events', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='resources',
            field=models.ManyToManyField(related_name=b'events', to='inventory.Resource', blank=True),
            preserve_default=True,
        ),
    ]
