# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Lock.creation_datetime'
        db.alter_column(u'lock_manager_lock', 'creation_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'Lock.creation_datetime'
        db.alter_column(u'lock_manager_lock', 'creation_datetime', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'lock_manager.lock': {
            'Meta': {'object_name': 'Lock'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'})
        }
    }

    complete_apps = ['lock_manager']
