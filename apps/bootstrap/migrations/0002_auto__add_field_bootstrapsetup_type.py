# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BootstrapSetup.type'
        db.add_column('bootstrap_bootstrapsetup', 'type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BootstrapSetup.type'
        db.delete_column('bootstrap_bootstrapsetup', 'type')


    models = {
        'bootstrap.bootstrapsetup': {
            'Meta': {'object_name': 'BootstrapSetup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fixture': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['bootstrap']