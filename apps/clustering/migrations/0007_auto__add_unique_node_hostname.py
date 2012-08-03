# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Node', fields ['hostname']
        db.create_unique('clustering_node', ['hostname'])


    def backwards(self, orm):
        # Removing unique constraint on 'Node', fields ['hostname']
        db.delete_unique('clustering_node', ['hostname'])


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
            'cpuload': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 3, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '4'})
        }
    }

    complete_apps = ['clustering']