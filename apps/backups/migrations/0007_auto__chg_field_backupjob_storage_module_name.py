# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BackupJob.storage_module_name'
        db.alter_column('backups_backupjob', 'storage_module_name', self.gf('django.db.models.fields.CharField')(max_length=32))

    def backwards(self, orm):

        # Changing field 'BackupJob.storage_module_name'
        db.alter_column('backups_backupjob', 'storage_module_name', self.gf('django.db.models.fields.CharField')(max_length=16))

    models = {
        'app_registry.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_registry.App']", 'symmetrical': 'False'}),
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 17, 0, 0)'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'storage_arguments_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'storage_module_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['backups']