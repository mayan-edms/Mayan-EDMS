# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.state'
        db.add_column('clustering_node', 'state',
                      self.gf('django.db.models.fields.CharField')(default='h', max_length=4),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node.state'
        db.delete_column('clustering_node', 'state')


    models = {
        'clustering.clusteringconfig': {
            'Meta': {'object_name': 'ClusteringConfig'},
            'dead_node_removal_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_id': ('django.db.models.fields.CharField', [], {'default': '1', 'unique': 'True', 'max_length': '1'}),
            'node_heartbeat_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'node_heartbeat_timeout': ('django.db.models.fields.PositiveIntegerField', [], {'default': '60'})
        },
        'clustering.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 2, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'h'", 'max_length': '4'})
        }
    }

    complete_apps = ['clustering']