# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field dependencies on 'App'
        db.delete_table('app_registry_app_dependencies')


    def backwards(self, orm):
        # Adding M2M table for field dependencies on 'App'
        db.create_table('app_registry_app_dependencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_app', models.ForeignKey(orm['app_registry.app'], null=False)),
            ('to_app', models.ForeignKey(orm['app_registry.app'], null=False))
        ))
        db.create_unique('app_registry_app_dependencies', ['from_app_id', 'to_app_id'])


    models = {
        'app_registry.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'app_registry.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_registry.App']", 'symmetrical': 'False'}),
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'storage_arguments_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'storage_module_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['app_registry']