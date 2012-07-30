# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('clustering_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cpuload', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('heartbeat', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 30, 0, 0), blank=True)),
            ('memory_usage', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('clustering', ['Node'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('clustering_node')


    models = {
        'clustering.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 30, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['clustering']