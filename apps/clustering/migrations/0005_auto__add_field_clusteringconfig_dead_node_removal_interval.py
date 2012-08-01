# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ClusteringConfig.dead_node_removal_interval'
        db.add_column('clustering_clusteringconfig', 'dead_node_removal_interval',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClusteringConfig.dead_node_removal_interval'
        db.delete_column('clustering_clusteringconfig', 'dead_node_removal_interval')


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
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 1, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'})
        }
    }

    complete_apps = ['clustering']