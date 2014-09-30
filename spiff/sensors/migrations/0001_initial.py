# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sensor'
        db.create_table(u'sensors_sensor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('ttl', self.gf('django.db.models.fields.IntegerField')(default=255)),
        ))
        db.send_create_signal(u'sensors', ['Sensor'])

        # Adding model 'SensorValue'
        db.create_table(u'sensors_sensorvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['sensors.Sensor'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sensors', ['SensorValue'])

        # Adding model 'Action'
        db.create_table(u'sensors_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['sensors.Sensor'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sensors', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Sensor'
        db.delete_table(u'sensors_sensor')

        # Deleting model 'SensorValue'
        db.delete_table(u'sensors_sensorvalue')

        # Deleting model 'Action'
        db.delete_table(u'sensors_action')


    models = {
        u'sensors.action': {
            'Meta': {'object_name': 'Action'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['sensors.Sensor']"}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'sensors.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ttl': ('django.db.models.fields.IntegerField', [], {'default': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'sensors.sensorvalue': {
            'Meta': {'ordering': "['-stamp']", 'object_name': 'SensorValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['sensors.Sensor']"}),
            'stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['sensors']