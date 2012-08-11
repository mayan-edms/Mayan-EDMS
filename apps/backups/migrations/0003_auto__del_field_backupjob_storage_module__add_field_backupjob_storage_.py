# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BackupJob.storage_module'
        db.delete_column('backups_backupjob', 'storage_module')

        # Adding field 'BackupJob.storage_module_name'
        db.add_column('backups_backupjob', 'storage_module_name',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=16),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'BackupJob.storage_module'
        raise RuntimeError("Cannot reverse this migration. 'BackupJob.storage_module' and its values cannot be restored.")
        # Deleting field 'BackupJob.storage_module_name'
        db.delete_column('backups_backupjob', 'storage_module_name')


    models = {
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)'}),
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