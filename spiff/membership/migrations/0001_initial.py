# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('payment', '0001_initial'),
        ('identity', '0001_initial'),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activeFromDate', models.DateTimeField(default=datetime.datetime(2014, 10, 27, 6, 55, 37, 505562))),
                ('activeToDate', models.DateTimeField(default=datetime.datetime(2014, 10, 27, 6, 55, 37, 505581))),
                ('identity', models.ForeignKey(related_name=b'membershipPeriods', to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('monthlyDues', models.FloatField(default=0)),
                ('isActiveMembership', models.BooleanField(default=False)),
                ('isKeyholder', models.BooleanField(default=False)),
                ('group', models.OneToOneField(to='auth.Group')),
            ],
            options={
                'permissions': (('can_change_identity_rank', 'Can change identity ranks'), ('can_view_identity_rank', 'Can view identity ranks'), ('can_deactivate_identity', 'Can deactivate an identity')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RankLineItem',
            fields=[
                ('lineitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='payment.LineItem')),
                ('activeFromDate', models.DateTimeField(default=datetime.datetime(2014, 10, 27, 6, 55, 37, 504924))),
                ('activeToDate', models.DateTimeField(default=datetime.datetime(2014, 10, 27, 6, 55, 37, 504946))),
                ('identity', models.ForeignKey(related_name=b'rankLineItems', to='identity.Identity')),
                ('rank', models.ForeignKey(to='membership.Rank')),
            ],
            options={
            },
            bases=('payment.lineitem',),
        ),
        migrations.CreateModel(
            name='RankSubscriptionPlan',
            fields=[
                ('subscriptionplan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='subscription.SubscriptionPlan')),
                ('quantity', models.IntegerField(default=1)),
                ('identity', models.ForeignKey(related_name=b'rankSubscriptions', blank=True, to='identity.Identity', null=True)),
                ('rank', models.ForeignKey(related_name=b'subscriptions', to='membership.Rank')),
            ],
            options={
            },
            bases=('subscription.subscriptionplan',),
        ),
        migrations.AddField(
            model_name='membershipperiod',
            name='lineItem',
            field=models.ForeignKey(default=None, blank=True, to='membership.RankLineItem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membershipperiod',
            name='rank',
            field=models.ForeignKey(to='membership.Rank'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='membershipperiod',
            index_together=set([('activeFromDate', 'activeToDate')]),
        ),
    ]
