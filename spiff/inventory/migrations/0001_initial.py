# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'inventory_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('trainable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'inventory', ['Resource'])

        # Adding model 'Metadata'
        db.create_table(u'inventory_metadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata', to=orm['inventory.Resource'])),
        ))
        db.send_create_signal(u'inventory', ['Metadata'])

        # Adding model 'TrainingLevel'
        db.create_table(u'inventory_traininglevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trainings', to=orm['identity.Identity'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trainings', to=orm['inventory.Resource'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'inventory', ['TrainingLevel'])

        # Adding model 'Certification'
        db.create_table(u'inventory_certification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='certifications', to=orm['identity.Identity'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='certifications', to=orm['inventory.Resource'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'inventory', ['Certification'])

        # Adding model 'Change'
        db.create_table(u'inventory_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changelog', to=orm['inventory.Resource'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['identity.Identity'])),
            ('trained_member', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='training_changes', null=True, to=orm['identity.Identity'])),
            ('old', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('new', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('property', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Change'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'inventory_resource')

        # Deleting model 'Metadata'
        db.delete_table(u'inventory_metadata')

        # Deleting model 'TrainingLevel'
        db.delete_table(u'inventory_traininglevel')

        # Deleting model 'Certification'
        db.delete_table(u'inventory_certification')

        # Deleting model 'Change'
        db.delete_table(u'inventory_change')


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
        u'identity.field': {
            'Meta': {'object_name': 'Field'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'identity.fieldvalue': {
            'Meta': {'object_name': 'FieldValue'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['identity.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': u"orm['identity.Identity']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'identity.identity': {
            'Meta': {'object_name': 'Identity'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'displayName': ('django.db.models.fields.TextField', [], {}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['identity.Field']", 'through': u"orm['identity.FieldValue']", 'symmetrical': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastSeen': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'member'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'inventory.certification': {
            'Meta': {'object_name': 'Certification'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certifications'", 'to': u"orm['identity.Identity']"}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certifications'", 'to': u"orm['inventory.Resource']"})
        },
        u'inventory.change': {
            'Meta': {'ordering': "['-stamp']", 'object_name': 'Change'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': u"orm['identity.Identity']"}),
            'new': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'property': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changelog'", 'to': u"orm['inventory.Resource']"}),
            'stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'trained_member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training_changes'", 'null': 'True', 'to': u"orm['identity.Identity']"})
        },
        u'inventory.metadata': {
            'Meta': {'object_name': 'Metadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': u"orm['inventory.Resource']"}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'inventory.resource': {
            'Meta': {'object_name': 'Resource'},
            'certified_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'certified_resources'", 'symmetrical': 'False', 'through': u"orm['inventory.Certification']", 'to': u"orm['identity.Identity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'trainable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['identity.Identity']", 'through': u"orm['inventory.TrainingLevel']", 'symmetrical': 'False'})
        },
        u'inventory.traininglevel': {
            'Meta': {'ordering': "['-rank']", 'object_name': 'TrainingLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trainings'", 'to': u"orm['identity.Identity']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trainings'", 'to': u"orm['inventory.Resource']"})
        }
    }

    complete_apps = ['inventory']