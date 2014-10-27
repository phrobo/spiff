# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('identity', models.ForeignKey(related_name=b'credits', to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('dueDate', models.DateField()),
                ('open', models.BooleanField(default=True)),
                ('draft', models.BooleanField(default=True)),
                ('identity', models.ForeignKey(related_name=b'invoices', to='identity.Identity')),
            ],
            options={
                'permissions': (('view_other_invoices', 'Can view invoices assigned to other identities'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineDiscountItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('flatRate', models.FloatField(default=0)),
                ('percent', models.FloatField(default=0)),
                ('invoice', models.ForeignKey(related_name=b'discounts', to='payment.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('unitPrice', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=1)),
                ('invoice', models.ForeignKey(related_name=b'items', to='payment.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Paid')])),
                ('transactionID', models.TextField(null=True, blank=True)),
                ('method', models.IntegerField(choices=[(0, b'Cash'), (1, b'Check'), (2, b'Stripe'), (3, b'Other'), (4, b'Credit')])),
                ('identity', models.ForeignKey(related_name=b'payments', to='identity.Identity')),
                ('invoice', models.ForeignKey(related_name=b'payments', to='payment.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StripeProxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripeID', models.TextField()),
                ('identity', models.ForeignKey(related_name=b'stripe', to='identity.Identity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='linediscountitem',
            name='lineItem',
            field=models.ForeignKey(related_name=b'discounts', to='payment.LineItem'),
            preserve_default=True,
        ),
    ]
