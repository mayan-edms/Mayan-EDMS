# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BackupJob'
        db.create_table('backups_backupjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('begin_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 11, 0, 0))),
            ('storage_module', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('storage_arguments_json', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('backups', ['BackupJob'])

        # Adding model 'BackupJobApp'
        db.create_table('backups_backupjobapp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('backup_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backups.BackupJob'])),
            ('app_backup', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('backups', ['BackupJobApp'])


    def backwards(self, orm):
        # Deleting model 'BackupJob'
        db.delete_table('backups_backupjob')

        # Deleting model 'BackupJobApp'
        db.delete_table('backups_backupjobapp')


    models = {
        'backups.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'begin_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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