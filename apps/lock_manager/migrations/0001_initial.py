# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lock'
        db.create_table('lock_manager_lock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=48)),
        ))
        db.send_create_signal('lock_manager', ['Lock'])


    def backwards(self, orm):
        # Deleting model 'Lock'
        db.delete_table('lock_manager_lock')


    models = {
        'lock_manager.lock': {
            'Meta': {'object_name': 'Lock'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'})
        }
    }

    complete_apps = ['lock_manager']