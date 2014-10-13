# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SpaceConfig'
        db.create_table(u'local_spaceconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('logo', self.gf('django.db.models.fields.CharField')(default='/logo.png', max_length=100)),
            ('openIcon', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('closedIcon', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('lastChange', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('motd', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'local', ['SpaceConfig'])

        # Adding model 'SpaceContact'
        db.create_table(u'local_spacecontact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['local.SpaceConfig'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'local', ['SpaceContact'])

        # Adding model 'SpaceFeed'
        db.create_table(u'local_spacefeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['local.SpaceConfig'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'local', ['SpaceFeed'])


    def backwards(self, orm):
        # Deleting model 'SpaceConfig'
        db.delete_table(u'local_spaceconfig')

        # Deleting model 'SpaceContact'
        db.delete_table(u'local_spacecontact')

        # Deleting model 'SpaceFeed'
        db.delete_table(u'local_spacefeed')


    models = {
        u'local.spaceconfig': {
            'Meta': {'object_name': 'SpaceConfig'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'closedIcon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChange': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'default': "'/logo.png'", 'max_length': '100'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'motd': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'openIcon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'local.spacecontact': {
            'Meta': {'object_name': 'SpaceContact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['local.SpaceConfig']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'local.spacefeed': {
            'Meta': {'object_name': 'SpaceFeed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['local.SpaceConfig']"}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['local']