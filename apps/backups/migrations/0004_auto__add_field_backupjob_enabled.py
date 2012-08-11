# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BackupJob.enabled'
        db.add_column('backups_backupjob', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BackupJob.enabled'
        db.delete_column('backups_backupjob', 'enabled')


    models = {
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'storage_arguments_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'storage_module_name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'backups.backupjobapp': {
            'Meta': {'object_name': 'BackupJobApp'},
            'app_backup': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'backup_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backups.BackupJob']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['backups']