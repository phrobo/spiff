# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owned_events', to=orm['membership.Member'])),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field attendees on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_attendees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('member', models.ForeignKey(orm[u'membership.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'member_id'])

        # Adding M2M table for field organizers on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_organizers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding M2M table for field resources on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_resources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('resource', models.ForeignKey(orm[u'inventory.resource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'resource_id'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field attendees on 'Event'
        db.delete_table(db.shorten_name(u'events_event_attendees'))

        # Removing M2M table for field organizers on 'Event'
        db.delete_table(db.shorten_name(u'events_event_organizers'))

        # Removing M2M table for field resources on 'Event'
        db.delete_table(db.shorten_name(u'events_event_resources'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'symmetrical': 'False', 'to': u"orm['membership.Member']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_events'", 'to': u"orm['membership.Member']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organized_events'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['inventory.Resource']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'inventory.certification': {
            'Meta': {'object_name': 'Certification'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certifications'", 'to': u"orm['membership.Member']"}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certifications'", 'to': u"orm['inventory.Resource']"})
        },
        u'inventory.resource': {
            'Meta': {'object_name': 'Resource'},
            'certified_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'certified_resources'", 'symmetrical': 'False', 'through': u"orm['inventory.Certification']", 'to': u"orm['membership.Member']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'trainable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['membership.Member']", 'through': u"orm['inventory.TrainingLevel']", 'symmetrical': 'False'})
        },
        u'inventory.traininglevel': {
            'Meta': {'ordering': "['-rank']", 'object_name': 'TrainingLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trainings'", 'to': u"orm['membership.Member']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trainings'", 'to': u"orm['inventory.Resource']"})
        },
        u'membership.field': {
            'Meta': {'object_name': 'Field'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'membership.fieldvalue': {
            'Meta': {'object_name': 'FieldValue'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': u"orm['membership.Member']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'membership.member': {
            'Meta': {'object_name': 'Member'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['membership.Field']", 'through': u"orm['membership.FieldValue']", 'symmetrical': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastSeen': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'stripeID': ('django.db.models.fields.TextField', [], {}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'member'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['events']