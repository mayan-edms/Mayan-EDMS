# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClusterSetting'
        db.create_table('smart_settings_clustersetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('smart_settings', ['ClusterSetting'])


    def backwards(self, orm):
        # Deleting model 'ClusterSetting'
        db.delete_table('smart_settings_clustersetting')


    models = {
        'smart_settings.clustersetting': {
            'Meta': {'object_name': 'ClusterSetting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['smart_settings']