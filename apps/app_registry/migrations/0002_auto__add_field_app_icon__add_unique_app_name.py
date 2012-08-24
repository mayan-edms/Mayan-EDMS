# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'App.icon'
        db.add_column('app_registry_app', 'icon',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'App', fields ['name']
        db.create_unique('app_registry_app', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'App', fields ['name']
        db.delete_unique('app_registry_app', ['name'])

        # Deleting field 'App.icon'
        db.delete_column('app_registry_app', 'icon')


    models = {
        'app_registry.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['app_registry']