# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('lineitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='payment.LineItem')),
            ],
            options={
            },
            bases=('payment.lineitem',),
        ),
        migrations.CreateModel(
            name='DonationSubscriptionPlan',
            fields=[
                ('subscriptionplan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='subscription.SubscriptionPlan')),
                ('value', models.FloatField()),
            ],
            options={
            },
            bases=('subscription.subscriptionplan',),
        ),
    ]
