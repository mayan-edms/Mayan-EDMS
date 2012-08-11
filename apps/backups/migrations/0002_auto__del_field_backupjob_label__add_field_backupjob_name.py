# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BackupJob.label'
        db.delete_column('backups_backupjob', 'label')

        # Adding field 'BackupJob.name'
        db.add_column('backups_backupjob', 'name',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=64),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'BackupJob.label'
        raise RuntimeError("Cannot reverse this migration. 'BackupJob.label' and its values cannot be restored.")
        # Deleting field 'BackupJob.name'
        db.delete_column('backups_backupjob', 'name')


    models = {
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'storage_arguments_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'storage_module': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'backups.backupjobapp': {
            'Meta': {'object_name': 'BackupJobApp'},
            'app_backup': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'backup_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backups.BackupJob']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['backups']