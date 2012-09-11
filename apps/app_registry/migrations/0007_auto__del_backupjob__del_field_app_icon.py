# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BackupJob'
        db.delete_table('app_registry_backupjob')

        # Removing M2M table for field apps on 'BackupJob'
        db.delete_table('app_registry_backupjob_apps')

        # Deleting field 'App.icon'
        db.delete_column('app_registry_app', 'icon')


    def backwards(self, orm):
        # Adding model 'BackupJob'
        db.create_table('app_registry_backupjob', (
            ('storage_arguments_json', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('storage_module_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('begin_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('app_registry', ['BackupJob'])

        # Adding M2M table for field apps on 'BackupJob'
        db.create_table('app_registry_backupjob_apps', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('backupjob', models.ForeignKey(orm['app_registry.backupjob'], null=False)),
            ('app', models.ForeignKey(orm['app_registry.app'], null=False))
        ))
        db.create_unique('app_registry_backupjob_apps', ['backupjob_id', 'app_id'])

        # Adding field 'App.icon'
        db.add_column('app_registry_app', 'icon',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)


    models = {
        'app_registry.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['app_registry.App']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['app_registry']