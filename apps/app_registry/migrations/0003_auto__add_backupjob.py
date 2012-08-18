# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BackupJob'
        db.create_table('app_registry_backupjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('begin_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('storage_module_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('storage_arguments_json', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app_registry', ['BackupJob'])

        # Adding M2M table for field apps on 'BackupJob'
        db.create_table('app_registry_backupjob_apps', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('backupjob', models.ForeignKey(orm['app_registry.backupjob'], null=False)),
            ('app', models.ForeignKey(orm['app_registry.app'], null=False))
        ))
        db.create_unique('app_registry_backupjob_apps', ['backupjob_id', 'app_id'])


    def backwards(self, orm):
        # Deleting model 'BackupJob'
        db.delete_table('app_registry_backupjob')

        # Removing M2M table for field apps on 'BackupJob'
        db.delete_table('app_registry_backupjob_apps')


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