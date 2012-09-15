# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ClusteringConfig'
        db.delete_table('clustering_clusteringconfig')


    def backwards(self, orm):
        # Adding model 'ClusteringConfig'
        db.create_table('clustering_clusteringconfig', (
            ('lock_id', self.gf('django.db.models.fields.CharField')(default=1, max_length=1, unique=True)),
            ('node_heartbeat_interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('dead_node_removal_interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('node_heartbeat_timeout', self.gf('django.db.models.fields.PositiveIntegerField')(default=60)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clustering', ['ClusteringConfig'])


    models = {
        'clustering.node': {
            'Meta': {'object_name': 'Node'},
            'cpuload': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'heartbeat': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 15, 0, 0)', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_usage': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '4'})
        }
    }

    complete_apps = ['clustering']